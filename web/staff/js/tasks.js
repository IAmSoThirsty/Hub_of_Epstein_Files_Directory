// Task Assignment System JavaScript

let selectedAgent = null;
let selectedPriority = 'medium';

// Agent selection
document.querySelectorAll('.agent-item').forEach(item => {
    item.addEventListener('click', function() {
        // Remove previous selection
        document.querySelectorAll('.agent-item').forEach(i => i.classList.remove('selected'));
        
        // Select this agent
        this.classList.add('selected');
        selectedAgent = this.dataset.agent;
        
        // Update form
        const agentName = this.querySelector('.agent-name').textContent;
        document.getElementById('selected-agent').value = agentName;
        
        // Enable submit button if form is valid
        validateForm();
    });
});

// Priority selection
document.querySelectorAll('.priority-option').forEach(option => {
    option.addEventListener('click', function() {
        // Remove previous selection
        document.querySelectorAll('.priority-option').forEach(o => o.classList.remove('selected'));
        
        // Select this priority
        this.classList.add('selected');
        selectedPriority = this.dataset.priority;
    });
});

// Form validation
function validateForm() {
    const title = document.getElementById('task-title').value.trim();
    const description = document.getElementById('task-description').value.trim();
    const submitBtn = document.getElementById('submit-task');
    
    if (selectedAgent && title && description) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}

// Listen to form inputs
document.getElementById('task-title').addEventListener('input', validateForm);
document.getElementById('task-description').addEventListener('input', validateForm);

// Submit task
document.getElementById('submit-task').addEventListener('click', function() {
    const taskData = {
        agent: selectedAgent,
        agentName: document.getElementById('selected-agent').value,
        title: document.getElementById('task-title').value,
        description: document.getElementById('task-description').value,
        priority: selectedPriority,
        volume: document.getElementById('task-volume').value || 'Not specified',
        deadline: document.getElementById('task-deadline').value || 'Not specified',
        assignedBy: 'Current User',
        timestamp: new Date().toISOString()
    };
    
    submitTask(taskData);
});

async function submitTask(taskData) {
    try {
        console.log('Submitting task:', taskData);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Show success message
        alert(`✅ Task successfully assigned to ${taskData.agentName}!\n\nThe task has been added to the queue with ${taskData.priority} priority.`);
        
        // Reset form
        document.getElementById('task-title').value = '';
        document.getElementById('task-description').value = '';
        document.getElementById('task-volume').value = '';
        document.getElementById('task-deadline').value = '';
        document.getElementById('selected-agent').value = '';
        
        // Remove agent selection
        document.querySelectorAll('.agent-item').forEach(i => i.classList.remove('selected'));
        selectedAgent = null;
        
        // Reset priority to medium
        document.querySelectorAll('.priority-option').forEach(o => o.classList.remove('selected'));
        document.querySelector('.priority-option.medium').classList.add('selected');
        selectedPriority = 'medium';
        
        // Disable submit button
        document.getElementById('submit-task').disabled = true;
        
        // Update queue display
        updateQueueDisplay(taskData);
        
        // Update agent queue count
        updateAgentQueueCount(taskData.agent);
        
    } catch (error) {
        console.error('Error submitting task:', error);
        alert('❌ Error submitting task. Please try again.');
    }
}

function updateQueueDisplay(taskData) {
    const recentTasks = document.getElementById('recent-tasks');
    const newTask = document.createElement('div');
    newTask.className = `queue-item priority-${taskData.priority}`;
    newTask.innerHTML = `
        <strong>${taskData.title}</strong> → ${taskData.agentName}<br>
        <small>Priority: ${taskData.priority.charAt(0).toUpperCase() + taskData.priority.slice(1)} | Status: Queued | Just added</small>
    `;
    recentTasks.prepend(newTask);
}

function updateAgentQueueCount(agentId) {
    const agentItem = document.querySelector(`.agent-item[data-agent="${agentId}"]`);
    if (agentItem) {
        const queueElement = agentItem.querySelector('.agent-queue');
        const currentCount = parseInt(queueElement.textContent.match(/\d+/)[0]);
        queueElement.textContent = `Queue: ${currentCount + 1} tasks pending`;
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Set default deadline to 7 days from now
    const defaultDeadline = new Date();
    defaultDeadline.setDate(defaultDeadline.getDate() + 7);
    document.getElementById('task-deadline').valueAsDate = defaultDeadline;
});
