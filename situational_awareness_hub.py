# situational_awareness_hub.py
import random
import os
import json
import datetime
import requests
from typing import Dict, List, Any, Optional

class SituationalAwarenessHub:
    """
    The SA Hub monitors cables or network infrastructure participating in HEIST.
    If a disruption is detected, it issues an alert to all interested nodes.
    Once conditions are restored, it notifies the DLR to terminate contracts.
    
    Now includes AI-powered predictive threat detection using Azure OpenAI.
    """
    def __init__(self):
        self.threat_detected = False
        self.alert_issued = False
        self.restored = False
        
        # Azure OpenAI configuration
        self.azure_api_key = os.environ.get("AZURE_API_KEY", "9abc905da5104e8eb8d6ec3ceb27f767")
        self.azure_endpoint = os.environ.get("AZURE_ENDPOINT", "https://aoai.apim.mitre.org/api-key")
        self.deployment_name = "gpt-4"
        
        # Threat intelligence database (simulated)
        self.threat_history = []
        self.threat_patterns = {}
        self.current_network_state = {}
        
        # Threat probability thresholds
        self.high_alert_threshold = 0.7
        self.medium_alert_threshold = 0.4

    def monitor_infrastructure(self):
        """
        Periodically check the infrastructure state (e.g., cables, satellites, etc.).
        Uses AI to analyze patterns and predict threats before they occur.
        """
        # Generate current network state (in a real system, this would be actual telemetry)
        self._update_network_state()
        
        # Use AI to analyze current state and predict threats
        threat_prediction = self._predict_threats()
        
        if threat_prediction:
            if not self.threat_detected and threat_prediction["probability"] > self.high_alert_threshold:
                self.threat_detected = True
                self.alert_issued = True
                print(f"\n[SA Hub] AI predicted threat: {threat_prediction['type']} with {threat_prediction['probability']:.2f} probability!")
                print(f"[SA Hub] Threat details: {threat_prediction['details']}")
                print("[SA Hub] Issuing alerts to all nodes...")
                
                # Log the threat for future analysis
                self._log_threat(threat_prediction)
            
            # Handle medium probability threats with warnings but no full alert
            elif not self.threat_detected and threat_prediction["probability"] > self.medium_alert_threshold:
                print(f"\n[SA Hub] AI warning: Potential {threat_prediction['type']} threat detected ({threat_prediction['probability']:.2f} probability)")
                print(f"[SA Hub] Monitoring closely: {threat_prediction['details']}")
        
        # Legacy random threat detection as fallback
        elif not self.threat_detected and random.choice([False, True, True]):
            self.threat_detected = True
            self.alert_issued = True
            print("\n[SA Hub] Threat detected! Issuing alerts to all nodes...")

        # If a threat is ongoing, use AI to evaluate if conditions are improving
        if self.threat_detected:
            resolution_prediction = self._predict_resolution()
            if resolution_prediction and resolution_prediction["probability"] > 0.65:
                self.threat_detected = False
                self.restored = True
                print(f"\n[SA Hub] AI predicts threat resolution with {resolution_prediction['probability']:.2f} confidence.")
                print(f"[SA Hub] Resolution details: {resolution_prediction['details']}")
                print("[SA Hub] Conditions restored. Signaling DLR to terminate contracts.")
            # Legacy random resolution as fallback
            elif random.choice([False, True]):
                self.threat_detected = False
                self.restored = True
                print("\n[SA Hub] Conditions restored. Signaling DLR to terminate contracts.")

    def _update_network_state(self):
        """
        Update the current network state with simulated telemetry data.
        In a real implementation, this would collect actual network metrics.
        """
        self.current_network_state = {
            "timestamp": datetime.datetime.now().isoformat(),
            "bandwidth_utilization": random.uniform(0.2, 0.95),
            "packet_loss_rate": random.uniform(0, 0.1),
            "latency_ms": random.uniform(5, 200),
            "node_health_metrics": {
                f"node_{i}": {
                    "cpu_usage": random.uniform(10, 90),
                    "memory_usage": random.uniform(20, 85),
                    "connection_count": random.randint(5, 2000),
                    "error_rate": random.uniform(0, 0.05)
                } for i in range(1, 6)
            },
            "environmental_conditions": {
                "solar_activity": random.uniform(0, 10),
                "weather_interference": random.uniform(0, 1),
                "geopolitical_risk_index": random.uniform(0, 5)
            }
        }

    def _predict_threats(self) -> Optional[Dict[str, Any]]:
        """
        Use Azure OpenAI to analyze current network state and predict potential threats.
        
        Returns:
            Dictionary containing threat prediction details or None if API call fails
        """
        try:
            # Prepare the network state as context
            network_context = json.dumps(self.current_network_state, indent=2)
            
            # Azure OpenAI API call
            headers = {
                "Content-Type": "application/json",
                "api-key": self.azure_api_key
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": "You are an advanced threat analysis system for satellite and ground station communications. Analyze the network state and identify potential threats or vulnerabilities. Respond with JSON containing threat type, probability (0-1), and detailed explanation."},
                    {"role": "user", "content": f"Analyze this network state data and predict potential threats:\n{network_context}\n\nRespond with only a JSON object containing 'type', 'probability', and 'details' fields."}
                ],
                "temperature": 0.3,
                "max_tokens": 800
            }
            
            # For simulation purposes, we'll generate a response without actually calling the API
            # In production, uncomment the following code and replace with actual endpoint
            
            # response = requests.post(
            #     f"{self.azure_endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version=2023-05-15",
            #     headers=headers,
            #     json=payload
            # )
            # response_data = response.json()
            # ai_response = response_data["choices"][0]["message"]["content"]
            
            # Simulated response for demo purposes
            threat_types = ["Denial of Service", "Signal Jamming", "Bandwidth Saturation", 
                           "Node Compromise", "Communication Interception", "Solar Flare Disruption"]
            
            # Generate threat probability based on network state
            probability = 0
            details = ""
            
            # Simple logic to simulate threat detection based on network metrics
            if self.current_network_state["packet_loss_rate"] > 0.07:
                probability += 0.3
                details += "Elevated packet loss rates indicate possible signal interference. "
            
            if self.current_network_state["bandwidth_utilization"] > 0.85:
                probability += 0.4
                details += "High bandwidth utilization suggests possible resource exhaustion attack. "
            
            if self.current_network_state["environmental_conditions"]["solar_activity"] > 7:
                probability += 0.5
                details += "High solar activity detected which may disrupt satellite communications. "
                
            if any(node["error_rate"] > 0.03 for node in self.current_network_state["node_health_metrics"].values()):
                probability += 0.35
                details += "Abnormal error rates on multiple nodes indicate possible systemic issue. "
                
            # Cap probability at 1.0
            probability = min(probability, 1.0)
            
            # Only return a threat if probability exceeds minimum threshold
            if probability > 0.2:
                threat_type = random.choice(threat_types)
                return {
                    "type": threat_type,
                    "probability": probability,
                    "details": details or f"Potential {threat_type.lower()} detected based on network metrics."
                }
            
            return None
            
        except Exception as e:
            print(f"[SA Hub] Error in threat prediction: {e}")
            return None

    def _predict_resolution(self) -> Optional[Dict[str, Any]]:
        """
        Use Azure OpenAI to predict if a current threat is being resolved.
        
        Returns:
            Dictionary containing resolution prediction details or None if API call fails
        """
        try:
            # Simple simulation of threat resolution prediction
            improvement_factors = []
            
            if self.current_network_state["packet_loss_rate"] < 0.05:
                improvement_factors.append("Packet loss rates returning to normal")
                
            if self.current_network_state["bandwidth_utilization"] < 0.7:
                improvement_factors.append("Bandwidth utilization stabilizing")
                
            if self.current_network_state["environmental_conditions"]["solar_activity"] < 5:
                improvement_factors.append("Solar activity decreasing")
                
            if all(node["error_rate"] < 0.02 for node in self.current_network_state["node_health_metrics"].values()):
                improvement_factors.append("Node error rates normalizing")
                
            # Calculate resolution probability based on improvement factors
            resolution_probability = min(len(improvement_factors) * 0.2, 1.0)
            
            if resolution_probability > 0.3 and improvement_factors:
                return {
                    "probability": resolution_probability,
                    "details": " ".join(improvement_factors)
                }
                
            return None
            
        except Exception as e:
            print(f"[SA Hub] Error in resolution prediction: {e}")
            return None

    def _log_threat(self, threat_data: Dict[str, Any]):
        """
        Log threat data to the threat history database for future analysis.
        """
        threat_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "network_state": self.current_network_state,
            "threat_data": threat_data
        }
        self.threat_history.append(threat_entry)
        
        # In a real system, this would persist to a database
        print(f"[SA Hub] Threat logged to database. Total threats recorded: {len(self.threat_history)}")

    def issue_alerts(self, all_nodes):
        """
        Sends an alert message to each node in the system.
        """
        if self.alert_issued:
            for node in all_nodes:
                node.receive_alert()
            # Reset after issuing alert
            self.alert_issued = False

    def reset_restored_flag(self):
        """
        Reset the 'restored' state after the DLR has taken action.
        """
        self.restored = False