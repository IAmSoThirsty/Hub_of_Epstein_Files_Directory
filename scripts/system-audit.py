#!/usr/bin/env python3
"""
System-Wide Military-Style Audit and Inspection Script

Performs comprehensive system audits including:
- Infrastructure status
- Agent performance and health
- Data integrity
- Security compliance
- Resource utilization
- Quality metrics
"""

import os
import sys
import json
import datetime
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Tuple
import hashlib


class SystemAuditor:
    """Comprehensive system audit and inspection manager"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or os.getcwd())
        self.timestamp = datetime.datetime.now()
        self.audit_results = {
            "audit_id": self._generate_audit_id(),
            "timestamp": self.timestamp.isoformat(),
            "audit_type": "system_wide_inspection",
            "classification": "INTERNAL USE",
            "sections": {}
        }
        
    def _generate_audit_id(self) -> str:
        """Generate unique audit ID"""
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return f"AUDIT-{ts}"
    
    def run_full_audit(self) -> Dict[str, Any]:
        """Execute complete system audit"""
        print("=" * 80)
        print("SYSTEM-WIDE MILITARY AUDIT AND INSPECTION")
        print("=" * 80)
        print(f"Audit ID: {self.audit_results['audit_id']}")
        print(f"Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("=" * 80)
        print()
        
        # Execute all audit sections
        self._audit_infrastructure()
        self._audit_agents()
        self._audit_data_integrity()
        self._audit_documentation()
        self._audit_security()
        self._audit_workflows()
        self._audit_scripts()
        self._audit_web_interface()
        self._audit_resources()
        
        # Generate overall status
        self._calculate_overall_status()
        
        return self.audit_results
    
    def _audit_infrastructure(self):
        """Audit core infrastructure components"""
        print("\n[1/9] INFRASTRUCTURE AUDIT")
        print("-" * 80)
        
        section = {
            "status": "OPERATIONAL",
            "components": {},
            "issues": [],
            "recommendations": []
        }
        
        # Check directory structure
        critical_dirs = [
            "data", "data/public_files", "data/processed", "data/wikipedia",
            "logs", "cache", "tmp", "scripts", "bots", "web", "docs"
        ]
        
        dir_status = []
        for dir_name in critical_dirs:
            dir_path = self.base_path / dir_name
            exists = dir_path.exists()
            writable = os.access(dir_path, os.W_OK) if exists else False
            
            status_item = {
                "path": dir_name,
                "exists": exists,
                "writable": writable,
                "status": "OK" if exists and writable else "ISSUE"
            }
            dir_status.append(status_item)
            
            if not exists:
                section["issues"].append(f"Missing directory: {dir_name}")
            elif not writable:
                section["issues"].append(f"Directory not writable: {dir_name}")
        
        section["components"]["directories"] = {
            "total": len(critical_dirs),
            "operational": sum(1 for d in dir_status if d["status"] == "OK"),
            "issues": sum(1 for d in dir_status if d["status"] == "ISSUE"),
            "details": dir_status
        }
        
        # Check critical files
        critical_files = [
            "README.md", "setup.py", "requirements.txt", "Makefile",
            "docker-compose.yml", "Dockerfile", ".env.example"
        ]
        
        file_status = []
        for file_name in critical_files:
            file_path = self.base_path / file_name
            exists = file_path.exists()
            readable = os.access(file_path, os.R_OK) if exists else False
            
            status_item = {
                "path": file_name,
                "exists": exists,
                "readable": readable,
                "status": "OK" if exists and readable else "ISSUE"
            }
            file_status.append(status_item)
            
            if not exists:
                section["issues"].append(f"Missing file: {file_name}")
        
        section["components"]["configuration_files"] = {
            "total": len(critical_files),
            "operational": sum(1 for f in file_status if f["status"] == "OK"),
            "issues": sum(1 for f in file_status if f["status"] == "ISSUE"),
            "details": file_status
        }
        
        # Check Python environment
        try:
            python_version = sys.version.split()[0]
            section["components"]["python"] = {
                "version": python_version,
                "status": "OK" if sys.version_info >= (3, 8) else "WARNING"
            }
        except Exception as e:
            section["issues"].append(f"Python check failed: {str(e)}")
        
        # Check Git status
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            section["components"]["git"] = {
                "uncommitted_changes": uncommitted,
                "status": "OK" if uncommitted == 0 else "WARNING"
            }
        except Exception as e:
            section["issues"].append(f"Git check failed: {str(e)}")
        
        if section["issues"]:
            section["status"] = "DEGRADED"
        
        self.audit_results["sections"]["infrastructure"] = section
        print(f"Status: {section['status']}")
        print(f"Issues Found: {len(section['issues'])}")
        
    def _audit_agents(self):
        """Audit AI agent infrastructure"""
        print("\n[2/9] AGENT INFRASTRUCTURE AUDIT")
        print("-" * 80)
        
        section = {
            "status": "OPERATIONAL",
            "agents": {},
            "issues": [],
            "recommendations": []
        }
        
        # Expected agent types
        agent_types = [
            "indexing-bot", "image-analysis-bot", "verification-bot",
            "search-bot", "summarization-bot", "pdf-analysis-bot",
            "cross-reference-bot", "entity-extraction-bot", "timeline-bot",
            "fact-checking-bot"
        ]
        
        bots_path = self.base_path / "bots"
        agent_status = []
        
        for agent in agent_types:
            agent_path = bots_path / agent
            readme_path = agent_path / "README.md"
            
            status_item = {
                "name": agent,
                "exists": agent_path.exists(),
                "documented": readme_path.exists() if agent_path.exists() else False,
                "status": "OK" if agent_path.exists() and readme_path.exists() else "ISSUE"
            }
            agent_status.append(status_item)
            
            if not agent_path.exists():
                section["issues"].append(f"Agent directory missing: {agent}")
            elif not readme_path.exists():
                section["issues"].append(f"Agent documentation missing: {agent}")
        
        section["agents"] = {
            "total_expected": len(agent_types),
            "operational": sum(1 for a in agent_status if a["status"] == "OK"),
            "issues": sum(1 for a in agent_status if a["status"] == "ISSUE"),
            "details": agent_status
        }
        
        # Check agent infrastructure documentation
        if (bots_path / "AGENT_INFRASTRUCTURE.md").exists():
            section["infrastructure_documented"] = True
        else:
            section["infrastructure_documented"] = False
            section["issues"].append("Agent infrastructure documentation missing")
        
        if section["issues"]:
            section["status"] = "DEGRADED"
        
        self.audit_results["sections"]["agents"] = section
        print(f"Status: {section['status']}")
        print(f"Agents Operational: {section['agents']['operational']}/{section['agents']['total_expected']}")
        
    def _audit_data_integrity(self):
        """Audit data integrity and storage"""
        print("\n[3/9] DATA INTEGRITY AUDIT")
        print("-" * 80)
        
        section = {
            "status": "OPERATIONAL",
            "storage": {},
            "issues": [],
            "recommendations": []
        }
        
        data_dirs = ["data", "data/public_files", "data/processed", "data/wikipedia"]
        
        for data_dir in data_dirs:
            dir_path = self.base_path / data_dir
            if dir_path.exists():
                # Count files
                try:
                    files = list(dir_path.rglob("*"))
                    file_count = len([f for f in files if f.is_file()])
                    
                    # Calculate size
                    total_size = sum(f.stat().st_size for f in files if f.is_file())
                    size_mb = total_size / (1024 * 1024)
                    
                    section["storage"][data_dir] = {
                        "files": file_count,
                        "size_mb": round(size_mb, 2),
                        "status": "OK"
                    }
                except Exception as e:
                    section["issues"].append(f"Error scanning {data_dir}: {str(e)}")
                    section["storage"][data_dir] = {
                        "status": "ERROR",
                        "error": str(e)
                    }
            else:
                section["storage"][data_dir] = {
                    "status": "MISSING",
                    "files": 0,
                    "size_mb": 0
                }
                section["issues"].append(f"Data directory missing: {data_dir}")
        
        if section["issues"]:
            section["status"] = "DEGRADED"
        
        self.audit_results["sections"]["data_integrity"] = section
        print(f"Status: {section['status']}")
        print(f"Data Directories: {len([d for d in section['storage'].values() if d.get('status') == 'OK'])}/{len(data_dirs)}")
        
    def _audit_documentation(self):
        """Audit documentation completeness"""
        print("\n[4/9] DOCUMENTATION AUDIT")
        print("-" * 80)
        
        section = {
            "status": "OPERATIONAL",
            "documents": {},
            "issues": [],
            "recommendations": []
        }
        
        required_docs = {
            "README.md": "Main documentation",
            "CONTRIBUTING.md": "Contribution guidelines",
            "SETUP_GUIDE.md": "Setup instructions",
            "docs/Glossary.md": "Terminology reference",
            "docs/CharacterDirectory.md": "Character index",
            "docs/Timeline.md": "Timeline documentation",
            "docs/Bot-Usage-Guide.md": "Bot documentation"
        }
        
        doc_status = []
        for doc_path, description in required_docs.items():
            full_path = self.base_path / doc_path
            exists = full_path.exists()
            
            if exists:
                size = full_path.stat().st_size
                status_item = {
                    "path": doc_path,
                    "description": description,
                    "exists": True,
                    "size_bytes": size,
                    "status": "OK" if size > 100 else "WARNING"
                }
                if size <= 100:
                    section["recommendations"].append(f"Document appears minimal: {doc_path}")
            else:
                status_item = {
                    "path": doc_path,
                    "description": description,
                    "exists": False,
                    "status": "MISSING"
                }
                section["issues"].append(f"Required document missing: {doc_path}")
            
            doc_status.append(status_item)
        
        section["documents"] = {
            "total_required": len(required_docs),
            "present": sum(1 for d in doc_status if d["exists"]),
            "missing": sum(1 for d in doc_status if not d["exists"]),
            "details": doc_status
        }
        
        if section["issues"]:
            section["status"] = "DEGRADED"
        
        self.audit_results["sections"]["documentation"] = section
        print(f"Status: {section['status']}")
        print(f"Documentation: {section['documents']['present']}/{section['documents']['total_required']}")
        
    def _audit_security(self):
        """Audit security configuration"""
        print("\n[5/9] SECURITY AUDIT")
        print("-" * 80)
        
        section = {
            "status": "OPERATIONAL",
            "checks": {},
            "issues": [],
            "recommendations": []
        }
        
        # Check for .env file (should not exist in repo)
        env_file = self.base_path / ".env"
        if env_file.exists():
            section["issues"].append("CRITICAL: .env file found in repository")
            section["checks"]["env_file"] = {
                "status": "CRITICAL",
                "message": ".env file should not be in version control"
            }
        else:
            section["checks"]["env_file"] = {
                "status": "OK",
                "message": "No .env file in repository"
            }
        
        # Check for .env.example
        env_example = self.base_path / ".env.example"
        if env_example.exists():
            section["checks"]["env_example"] = {
                "status": "OK",
                "message": ".env.example template present"
            }
        else:
            section["recommendations"].append("Add .env.example for environment configuration")
            section["checks"]["env_example"] = {
                "status": "WARNING",
                "message": ".env.example template missing"
            }
        
        # Check .gitignore
        gitignore = self.base_path / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text()
            has_env = ".env" in content or "*.env" in content
            has_secrets = "secret" in content.lower() or "password" in content.lower()
            
            section["checks"]["gitignore"] = {
                "status": "OK" if has_env else "WARNING",
                "message": "Properly configured" if has_env else "Should ignore .env files",
                "protects_env": has_env,
                "protects_secrets": has_secrets
            }
            
            if not has_env:
                section["recommendations"].append("Add .env to .gitignore")
        else:
            section["issues"].append("No .gitignore file found")
        
        # Check for common sensitive file patterns
        sensitive_patterns = ["*.key", "*.pem", "*.p12", "*password*", "*secret*"]
        found_sensitive = []
        for pattern in sensitive_patterns:
            matches = list(self.base_path.glob(pattern))
            if matches:
                found_sensitive.extend([str(m.relative_to(self.base_path)) for m in matches[:5]])
        
        if found_sensitive:
            section["issues"].append(f"Potentially sensitive files found: {', '.join(found_sensitive)}")
            section["checks"]["sensitive_files"] = {
                "status": "WARNING",
                "count": len(found_sensitive),
                "examples": found_sensitive[:5]
            }
        else:
            section["checks"]["sensitive_files"] = {
                "status": "OK",
                "message": "No obvious sensitive files detected"
            }
        
        if any("CRITICAL" in str(c) for c in section["checks"].values()):
            section["status"] = "CRITICAL"
        elif section["issues"]:
            section["status"] = "DEGRADED"
        
        self.audit_results["sections"]["security"] = section
        print(f"Status: {section['status']}")
        print(f"Security Issues: {len(section['issues'])}")
        
    def _audit_workflows(self):
        """Audit GitHub Actions workflows"""
        print("\n[6/9] WORKFLOW AUDIT")
        print("-" * 80)
        
        section = {
            "status": "OPERATIONAL",
            "workflows": {},
            "issues": [],
            "recommendations": []
        }
        
        workflows_dir = self.base_path / ".github" / "workflows"
        
        if workflows_dir.exists():
            workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
            
            workflow_details = []
            for wf in workflow_files:
                workflow_details.append({
                    "name": wf.name,
                    "size_bytes": wf.stat().st_size,
                    "status": "OK"
                })
            
            section["workflows"] = {
                "total": len(workflow_files),
                "details": workflow_details
            }
            
            # Check for key workflows
            expected_workflows = [
                "agent-monitoring.yml",
                "verify-setup.yml",
                "deploy-pages.yml"
            ]
            
            existing_names = [wf.name for wf in workflow_files]
            for expected in expected_workflows:
                if expected not in existing_names:
                    section["recommendations"].append(f"Consider adding workflow: {expected}")
        else:
            section["issues"].append("GitHub workflows directory not found")
            section["status"] = "DEGRADED"
        
        self.audit_results["sections"]["workflows"] = section
        print(f"Status: {section['status']}")
        print(f"Workflows: {section['workflows'].get('total', 0)}")
        
    def _audit_scripts(self):
        """Audit Python scripts"""
        print("\n[7/9] SCRIPTS AUDIT")
        print("-" * 80)
        
        section = {
            "status": "OPERATIONAL",
            "scripts": {},
            "issues": [],
            "recommendations": []
        }
        
        scripts_dir = self.base_path / "scripts"
        
        if scripts_dir.exists():
            script_files = list(scripts_dir.glob("*.py"))
            
            script_details = []
            for script in script_files:
                is_executable = os.access(script, os.X_OK)
                size = script.stat().st_size
                
                script_details.append({
                    "name": script.name,
                    "size_bytes": size,
                    "executable": is_executable,
                    "status": "OK" if size > 0 else "WARNING"
                })
                
                if size == 0:
                    section["issues"].append(f"Empty script: {script.name}")
            
            section["scripts"] = {
                "total": len(script_files),
                "operational": sum(1 for s in script_details if s["status"] == "OK"),
                "details": script_details
            }
        else:
            section["issues"].append("Scripts directory not found")
            section["status"] = "DEGRADED"
        
        self.audit_results["sections"]["scripts"] = section
        print(f"Status: {section['status']}")
        print(f"Scripts: {section['scripts'].get('total', 0)}")
        
    def _audit_web_interface(self):
        """Audit web interface"""
        print("\n[8/9] WEB INTERFACE AUDIT")
        print("-" * 80)
        
        section = {
            "status": "OPERATIONAL",
            "pages": {},
            "issues": [],
            "recommendations": []
        }
        
        web_dir = self.base_path / "web"
        
        if web_dir.exists():
            # Check for HTML pages
            html_files = list(web_dir.glob("*.html")) + list(web_dir.rglob("*.html"))
            
            # Check for JavaScript
            js_files = list(web_dir.rglob("*.js"))
            
            # Check for CSS
            css_files = list(web_dir.rglob("*.css"))
            
            section["pages"] = {
                "html_files": len(html_files),
                "js_files": len(js_files),
                "css_files": len(css_files),
                "status": "OK"
            }
            
            if len(html_files) == 0:
                section["issues"].append("No HTML files found in web directory")
                section["status"] = "DEGRADED"
        else:
            section["issues"].append("Web directory not found")
            section["status"] = "DEGRADED"
        
        self.audit_results["sections"]["web_interface"] = section
        print(f"Status: {section['status']}")
        print(f"HTML Pages: {section['pages'].get('html_files', 0)}")
        
    def _audit_resources(self):
        """Audit resource utilization"""
        print("\n[9/9] RESOURCE UTILIZATION AUDIT")
        print("-" * 80)
        
        section = {
            "status": "OPERATIONAL",
            "resources": {},
            "issues": [],
            "recommendations": []
        }
        
        # Calculate total repository size
        try:
            total_size = 0
            file_count = 0
            
            for item in self.base_path.rglob("*"):
                if item.is_file() and ".git" not in str(item):
                    total_size += item.stat().st_size
                    file_count += 1
            
            size_mb = total_size / (1024 * 1024)
            size_gb = size_mb / 1024
            
            section["resources"]["repository"] = {
                "total_files": file_count,
                "total_size_mb": round(size_mb, 2),
                "total_size_gb": round(size_gb, 2),
                "status": "OK" if size_gb < 50 else "WARNING"
            }
            
            if size_gb > 50:
                section["recommendations"].append(f"Repository size ({size_gb:.2f} GB) is large. Consider cleanup.")
        except Exception as e:
            section["issues"].append(f"Error calculating repository size: {str(e)}")
        
        # Check logs directory size
        logs_dir = self.base_path / "logs"
        if logs_dir.exists():
            try:
                logs_size = sum(f.stat().st_size for f in logs_dir.rglob("*") if f.is_file())
                logs_mb = logs_size / (1024 * 1024)
                
                section["resources"]["logs"] = {
                    "size_mb": round(logs_mb, 2),
                    "status": "OK" if logs_mb < 1000 else "WARNING"
                }
                
                if logs_mb > 1000:
                    section["recommendations"].append(f"Logs directory ({logs_mb:.2f} MB) should be cleaned up")
            except Exception as e:
                section["issues"].append(f"Error checking logs: {str(e)}")
        
        # Check cache directory size
        cache_dir = self.base_path / "cache"
        if cache_dir.exists():
            try:
                cache_size = sum(f.stat().st_size for f in cache_dir.rglob("*") if f.is_file())
                cache_mb = cache_size / (1024 * 1024)
                
                section["resources"]["cache"] = {
                    "size_mb": round(cache_mb, 2),
                    "status": "OK" if cache_mb < 5000 else "WARNING"
                }
                
                if cache_mb > 5000:
                    section["recommendations"].append(f"Cache directory ({cache_mb:.2f} MB) should be cleaned up")
            except Exception as e:
                section["issues"].append(f"Error checking cache: {str(e)}")
        
        if section["issues"]:
            section["status"] = "DEGRADED"
        
        self.audit_results["sections"]["resources"] = section
        print(f"Status: {section['status']}")
        print(f"Total Files: {section['resources'].get('repository', {}).get('total_files', 'N/A')}")
        
    def _calculate_overall_status(self):
        """Calculate overall system status"""
        statuses = [section.get("status", "UNKNOWN") for section in self.audit_results["sections"].values()]
        
        if "CRITICAL" in statuses:
            overall = "CRITICAL"
        elif "DEGRADED" in statuses:
            overall = "DEGRADED"
        elif "WARNING" in statuses:
            overall = "WARNING"
        elif all(s == "OPERATIONAL" for s in statuses):
            overall = "OPERATIONAL"
        else:
            overall = "UNKNOWN"
        
        self.audit_results["overall_status"] = overall
        
        # Count issues
        total_issues = sum(len(section.get("issues", [])) for section in self.audit_results["sections"].values())
        total_recommendations = sum(len(section.get("recommendations", [])) for section in self.audit_results["sections"].values())
        
        self.audit_results["summary"] = {
            "total_sections": len(self.audit_results["sections"]),
            "total_issues": total_issues,
            "total_recommendations": total_recommendations,
            "overall_status": overall
        }
        
    def generate_report(self, format_type: str = "markdown") -> str:
        """Generate formatted audit report"""
        if format_type == "markdown":
            return self._generate_markdown_report()
        elif format_type == "json":
            return json.dumps(self.audit_results, indent=2)
        else:
            return self._generate_text_report()
    
    def _generate_markdown_report(self) -> str:
        """Generate markdown formatted report"""
        lines = []
        
        lines.append("# SYSTEM-WIDE MILITARY AUDIT AND INSPECTION REPORT")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"**Audit ID:** {self.audit_results['audit_id']}")
        lines.append(f"**Timestamp:** {self.audit_results['timestamp']}")
        lines.append(f"**Classification:** {self.audit_results['classification']}")
        lines.append(f"**Overall Status:** {self.audit_results['overall_status']}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Executive Summary
        lines.append("## EXECUTIVE SUMMARY")
        lines.append("")
        summary = self.audit_results.get("summary", {})
        lines.append(f"- **Total Sections Audited:** {summary.get('total_sections', 0)}")
        lines.append(f"- **Total Issues Found:** {summary.get('total_issues', 0)}")
        lines.append(f"- **Total Recommendations:** {summary.get('total_recommendations', 0)}")
        lines.append(f"- **System Status:** {summary.get('overall_status', 'UNKNOWN')}")
        lines.append("")
        
        # Detailed Sections
        for section_name, section_data in self.audit_results["sections"].items():
            lines.append(f"## {section_name.upper().replace('_', ' ')}")
            lines.append("")
            lines.append(f"**Status:** {section_data.get('status', 'UNKNOWN')}")
            lines.append("")
            
            # Issues
            issues = section_data.get("issues", [])
            if issues:
                lines.append("### Issues")
                for issue in issues:
                    lines.append(f"- ⚠️ {issue}")
                lines.append("")
            
            # Recommendations
            recommendations = section_data.get("recommendations", [])
            if recommendations:
                lines.append("### Recommendations")
                for rec in recommendations:
                    lines.append(f"- 💡 {rec}")
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        # Footer
        lines.append("## AUDIT CERTIFICATION")
        lines.append("")
        lines.append(f"This audit was conducted automatically on {self.timestamp.strftime('%Y-%m-%d at %H:%M:%S UTC')}.")
        lines.append("All findings are based on automated checks and should be verified by human operators.")
        lines.append("")
        lines.append("**END OF REPORT**")
        
        return "\n".join(lines)
    
    def _generate_text_report(self) -> str:
        """Generate plain text report"""
        lines = []
        
        lines.append("=" * 80)
        lines.append("SYSTEM-WIDE MILITARY AUDIT AND INSPECTION REPORT")
        lines.append("=" * 80)
        lines.append(f"Audit ID: {self.audit_results['audit_id']}")
        lines.append(f"Timestamp: {self.audit_results['timestamp']}")
        lines.append(f"Classification: {self.audit_results['classification']}")
        lines.append(f"Overall Status: {self.audit_results['overall_status']}")
        lines.append("=" * 80)
        lines.append("")
        
        summary = self.audit_results.get("summary", {})
        lines.append("EXECUTIVE SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total Sections Audited: {summary.get('total_sections', 0)}")
        lines.append(f"Total Issues Found: {summary.get('total_issues', 0)}")
        lines.append(f"Total Recommendations: {summary.get('total_recommendations', 0)}")
        lines.append(f"System Status: {summary.get('overall_status', 'UNKNOWN')}")
        lines.append("")
        
        for section_name, section_data in self.audit_results["sections"].items():
            lines.append("-" * 80)
            lines.append(f"{section_name.upper().replace('_', ' ')}")
            lines.append("-" * 80)
            lines.append(f"Status: {section_data.get('status', 'UNKNOWN')}")
            
            issues = section_data.get("issues", [])
            if issues:
                lines.append("\nIssues:")
                for issue in issues:
                    lines.append(f"  - {issue}")
            
            recommendations = section_data.get("recommendations", [])
            if recommendations:
                lines.append("\nRecommendations:")
                for rec in recommendations:
                    lines.append(f"  - {rec}")
            
            lines.append("")
        
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def save_report(self, output_dir: str = "logs", format_type: str = "markdown"):
        """Save audit report to file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp_str = self.timestamp.strftime("%Y%m%d_%H%M%S")
        
        # Save markdown report
        if format_type in ["markdown", "all"]:
            md_file = output_path / f"system_audit_{timestamp_str}.md"
            md_file.write_text(self._generate_markdown_report())
            print(f"\n✅ Markdown report saved: {md_file}")
        
        # Save JSON report
        if format_type in ["json", "all"]:
            json_file = output_path / f"system_audit_{timestamp_str}.json"
            json_file.write_text(json.dumps(self.audit_results, indent=2))
            print(f"✅ JSON report saved: {json_file}")
        
        # Save text report
        if format_type in ["text", "all"]:
            txt_file = output_path / f"system_audit_{timestamp_str}.txt"
            txt_file.write_text(self._generate_text_report())
            print(f"✅ Text report saved: {txt_file}")


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="System-Wide Military Audit and Inspection Tool"
    )
    parser.add_argument(
        "--output-dir",
        default="logs",
        help="Directory to save audit reports (default: logs)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "text", "all"],
        default="markdown",
        help="Report format (default: markdown)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress console output"
    )
    
    args = parser.parse_args()
    
    # Run audit
    auditor = SystemAuditor()
    
    if not args.quiet:
        auditor.run_full_audit()
    else:
        # Redirect stdout temporarily
        import io
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        auditor.run_full_audit()
        sys.stdout = old_stdout
    
    # Save reports
    auditor.save_report(output_dir=args.output_dir, format_type=args.format)
    
    # Print summary
    print("\n" + "=" * 80)
    print("AUDIT COMPLETE")
    print("=" * 80)
    print(f"Audit ID: {auditor.audit_results['audit_id']}")
    print(f"Overall Status: {auditor.audit_results['overall_status']}")
    print(f"Issues Found: {auditor.audit_results['summary']['total_issues']}")
    print(f"Recommendations: {auditor.audit_results['summary']['total_recommendations']}")
    print("=" * 80)
    
    # Return exit code based on status
    if auditor.audit_results['overall_status'] == "CRITICAL":
        return 2
    elif auditor.audit_results['overall_status'] == "DEGRADED":
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
