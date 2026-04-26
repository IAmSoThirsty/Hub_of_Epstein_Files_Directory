/* eslint-env browser */
/* global window, document, fetch, FormData, prompt, setInterval, clearInterval */
// Upload client for authenticated admin document submissions

const UPLOAD_API_BASE_URL = window.EPSTEIN_API_BASE_URL || "";
const MAX_UPLOAD_SIZE_BYTES = 100 * 1024 * 1024;
let adminSessionReady = false;
let sessionPromptInFlight = false;

function getUploadEndpoint(path) {
    return `${UPLOAD_API_BASE_URL}${path}`;
}

async function establishAdminSession(forcePrompt = false) {
    if (adminSessionReady && !forcePrompt) {
        return true;
    }

    if (sessionPromptInFlight) {
        return false;
    }

    sessionPromptInFlight = true;
    try {
        const token = prompt(
            "Enter admin API token to establish a secure upload session:",
        );
        if (!token || !token.trim()) {
            appendStatusMessage(
                "Upload cancelled: admin session token not provided.",
                "warning",
            );
            return false;
        }

        const response = await fetch(getUploadEndpoint("/api/v1/auth/session"), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({ adminToken: token.trim() }),
        });

        if (!response.ok) {
            const body = await response
                .json()
                .catch(() => ({ detail: "Authentication failed" }));
            throw new Error(body.detail || "Authentication failed");
        }

        adminSessionReady = true;
        appendStatusMessage("Secure admin session established.", "success");
        return true;
    } catch (error) {
        adminSessionReady = false;
        appendStatusMessage(error.message, "error");
        return false;
    } finally {
        sessionPromptInFlight = false;
    }
}

async function fetchWithAdminSession(path, options = {}, allowRetry = true) {
    const requestOptions = {
        ...options,
        credentials: "include",
    };

    let response = await fetch(getUploadEndpoint(path), requestOptions);

    if (response.status === 401 && allowRetry) {
        adminSessionReady = false;
        const sessionEstablished = await establishAdminSession(true);
        if (!sessionEstablished) {
            return response;
        }

        response = await fetch(getUploadEndpoint(path), requestOptions);
    }

    return response;
}

function appendStatusMessage(message, level = "info") {
    const statusContainer = document.getElementById("upload-status");
    const messages = document.getElementById("status-messages");
    if (!statusContainer || !messages) {
        return;
    }

    statusContainer.style.display = "block";

    const line = document.createElement("div");
    line.className = `status-message status-${level}`;
    line.textContent = message;
    messages.prepend(line);
}

function upsertQueueItem(jobId, payload) {
    const queue = document.getElementById("upload-queue");
    const queueItems = document.getElementById("queue-items");
    if (!queue || !queueItems) {
        return;
    }

    queue.style.display = "block";

    let item = document.getElementById(`job-${jobId}`);
    if (!item) {
        item = document.createElement("div");
        item.id = `job-${jobId}`;
        item.className = "upload-queue-item";
        queueItems.prepend(item);
    }

    item.innerHTML = `
        <div><strong>${payload.filename || "upload.pdf"}</strong></div>
        <div>Status: ${payload.status}</div>
        ${payload.decision ? `<div>Decision: ${payload.decision}</div>` : ""}
        ${payload.relevanceScore !== undefined ? `<div>Relevance: ${payload.relevanceScore}</div>` : ""}
    `;
}

function validateFile(file) {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
        appendStatusMessage(`${file.name} rejected: only PDF files are allowed.`, "error");
        return false;
    }

    if (file.size > MAX_UPLOAD_SIZE_BYTES) {
        appendStatusMessage(`${file.name} rejected: file exceeds 100MB.`, "error");
        return false;
    }

    return true;
}

async function submitUpload(file) {
    const sessionEstablished = await establishAdminSession();
    if (!sessionEstablished) {
        appendStatusMessage(
            "Upload cancelled: admin session could not be established.",
            "warning",
        );
        return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("source", "web-upload");
    formData.append("metadata", JSON.stringify({
        client: "web",
        uploadedAt: new Date().toISOString(),
    }));

    try {
        const response = await fetchWithAdminSession("/api/v1/upload", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const body = await response.json().catch(() => ({ detail: "Upload failed" }));
            throw new Error(body.detail || "Upload failed");
        }

        const payload = await response.json();
        appendStatusMessage(`Queued ${file.name} (job ${payload.jobId}).`, "success");
        upsertQueueItem(payload.jobId, {
            filename: file.name,
            status: payload.status,
        });

        pollJobStatus(payload.jobId, file.name);
    } catch (error) {
        appendStatusMessage(`${file.name}: ${error.message}`, "error");
    }
}

function pollJobStatus(jobId, filename) {
    const pollHandle = setInterval(async () => {
        try {
            const response = await fetchWithAdminSession(
                `/api/v1/upload/${jobId}`,
                { method: "GET" },
            );

            if (!response.ok) {
                throw new Error("Unable to fetch upload job status");
            }

            const payload = await response.json();
            upsertQueueItem(jobId, {
                filename,
                status: payload.status,
                decision: payload.result?.decision,
                relevanceScore: payload.result?.relevanceScore,
            });

            if (payload.status === "completed") {
                appendStatusMessage(
                    `${filename} processed: ${payload.result?.decision} (${payload.result?.relevanceScore}).`,
                    "success",
                );
                clearInterval(pollHandle);
            }

            if (payload.status === "failed") {
                appendStatusMessage(`${filename} failed: ${payload.error || "unknown error"}`, "error");
                clearInterval(pollHandle);
            }
        } catch (error) {
            appendStatusMessage(`${filename}: ${error.message}`, "error");
            clearInterval(pollHandle);
        }
    }, 2000);
}

async function handleFileList(fileList) {
    const validFiles = Array.from(fileList).filter(validateFile);
    for (const file of validFiles) {
        // eslint-disable-next-line no-await-in-loop
        await submitUpload(file);
    }
}

function bindUploadEvents() {
    const uploadInput = document.getElementById("pdf-upload");
    const uploadZone = document.getElementById("upload-zone");

    if (!uploadInput || !uploadZone) {
        return;
    }

    uploadInput.addEventListener("change", (event) => {
        if (event.target.files) {
            handleFileList(event.target.files);
        }
    });

    ["dragenter", "dragover"].forEach((eventName) => {
        uploadZone.addEventListener(eventName, (event) => {
            event.preventDefault();
            uploadZone.classList.add("drag-over");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        uploadZone.addEventListener(eventName, (event) => {
            event.preventDefault();
            uploadZone.classList.remove("drag-over");
        });
    });

    uploadZone.addEventListener("drop", (event) => {
        if (event.dataTransfer?.files) {
            handleFileList(event.dataTransfer.files);
        }
    });
}

document.addEventListener("DOMContentLoaded", bindUploadEvents);
