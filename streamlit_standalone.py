import streamlit as st
import json
import random
import time
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="HEIST Simulation Demo",
    page_icon="🛰️",
    layout="wide"
)

# Title and description
st.title("HEIST Simulation Dashboard")
st.subheader("Hybrid Space/Submarine Architecture Ensuring Infosec of Telecommunications")

# Information about the unavailable full version
st.info("""
**Note:** This is a lightweight demo version of the HEIST simulation dashboard. 
To run the full application with all features, please clone the repository and run locally with the required dependencies.
""")

# Configuration sidebar
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Azure API Key", type="password")
api_endpoint = st.sidebar.text_input("Azure Endpoint")

# Simulation parameters
num_cycles = st.sidebar.slider("Simulation Cycles", 1, 20, 5)
simulation_speed = st.sidebar.slider("Simulation Speed", 0.1, 2.0, 1.0)
advanced_options = st.sidebar.expander("Advanced Options")

with advanced_options:
    high_alert_threshold = st.slider("High Alert Threshold", 0.5, 0.9, 0.7, 0.05)
    medium_alert_threshold = st.slider("Medium Alert Threshold", 0.2, 0.6, 0.4, 0.05)
    threat_randomness = st.slider("Threat Randomness", 0.1, 1.0, 0.5, 0.1)

# Mock data generator functions
def generate_network_state():
    return {
        "timestamp": datetime.now().isoformat(),
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

def generate_threat(network_state):
    threat_types = [
        "Denial of Service", 
        "Signal Jamming", 
        "Bandwidth Saturation",
        "Node Compromise", 
        "Communication Interception", 
        "Solar Flare Disruption"
    ]
    
    # Calculate probability based on network state
    probability = 0
    details = ""
    
    if network_state["packet_loss_rate"] > 0.07:
        probability += 0.3
        details += "Elevated packet loss rates indicate possible signal interference. "
    
    if network_state["bandwidth_utilization"] > 0.85:
        probability += 0.4
        details += "High bandwidth utilization suggests possible resource exhaustion attack. "
    
    if network_state["environmental_conditions"]["solar_activity"] > 7:
        probability += 0.5
        details += "High solar activity detected which may disrupt satellite communications. "
        
    if any(node["error_rate"] > 0.03 for node in network_state["node_health_metrics"].values()):
        probability += 0.35
        details += "Abnormal error rates on multiple nodes indicate possible systemic issue. "
    
    # Add some randomness
    probability = min(probability + random.uniform(-0.1, 0.1), 1.0)
    
    # Only return a threat if probability exceeds minimum threshold
    if probability > 0.2:
        threat_type = random.choice(threat_types)
        return {
            "timestamp": network_state["timestamp"],
            "network_state": network_state,
            "threat_data": {
                "type": threat_type,
                "probability": probability,
                "details": details or f"Potential {threat_type.lower()} detected based on network metrics."
            }
        }
    
    return None

def generate_log_entry(cycle, network_state, threat_data=None):
    log = f"\n=== Simulation Cycle {cycle} ===\n"
    
    if threat_data and threat_data["threat_data"]["probability"] > high_alert_threshold:
        log += f"[SA Hub] AI predicted threat: {threat_data['threat_data']['type']} with {threat_data['threat_data']['probability']:.2f} probability!\n"
        log += f"[SA Hub] Threat details: {threat_data['threat_data']['details']}\n"
        log += "[SA Hub] Issuing alerts to all nodes...\n"
        log += f"[RoutingHub] Creating contract for emergency routing\n"
        log += f"[RoutingHub] Selected node_3 for emergency routing based on availability\n"
    elif threat_data and threat_data["threat_data"]["probability"] > medium_alert_threshold:
        log += f"[SA Hub] AI warning: Potential {threat_data['threat_data']['type']} threat detected ({threat_data['threat_data']['probability']:.2f} probability)\n"
        log += f"[SA Hub] Monitoring closely: {threat_data['threat_data']['details']}\n"
    
    log += f"[Node_1] Processing tasks: 3 active connections\n"
    log += f"[Node_2] Processing tasks: 5 active connections\n"
    log += f"[RoutingHub] Current bandwidth utilization: {network_state['bandwidth_utilization']:.2f}\n"
    
    # Random events
    events = [
        "Received new data request from GroundStation2 to Satellite1",
        "Contract 1842 executed successfully",
        "Handshake verified for Node_3",
        "Smart contract deployment successful",
        "Security classification verified for high-priority message"
    ]
    
    log += f"[System] {random.choice(events)}\n"
    
    return log

def run_simulation():
    # Initialize state storage
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    if 'threats' not in st.session_state:
        st.session_state.threats = []
    if 'metrics' not in st.session_state:
        st.session_state.metrics = {
            'bandwidth_utilization': [],
            'packet_loss': [],
            'latency': [],
            'threats_detected': 0,
            'contracts_created': 0,
            'contracts_terminated': 0,
        }
    
    # Create placeholders for UI updates
    output_placeholder = st.empty()
    network_state_placeholder = st.empty()
    metrics_placeholder = st.empty()
    threats_placeholder = st.empty()
    
    # Run simulation cycles
    for cycle in range(1, num_cycles + 1):
        # Generate data for this cycle
        current_state = generate_network_state()
        threat_data = generate_threat(current_state)
        
        # Generate log entry
        log_entry = generate_log_entry(cycle, current_state, threat_data)
        st.session_state.logs.append(log_entry)
        
        # Update metrics
        st.session_state.metrics['bandwidth_utilization'].append(current_state['bandwidth_utilization'])
        st.session_state.metrics['packet_loss'].append(current_state['packet_loss_rate'])
        st.session_state.metrics['latency'].append(current_state['latency_ms'])
        
        # Check if this was a threat cycle
        if threat_data:
            if threat_data["threat_data"]["probability"] > high_alert_threshold:
                st.session_state.metrics['threats_detected'] += 1
                st.session_state.metrics['contracts_created'] += 1
                st.session_state.threats.append(threat_data)
            elif threat_data["threat_data"]["probability"] > medium_alert_threshold:
                st.session_state.threats.append(threat_data)
        
        # Update UI
        # Display the full log
        output_placeholder.text_area("Simulation Log", "\n".join(st.session_state.logs[-5:]), height=300)
        
        # Display current network state
        with network_state_placeholder.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Current Network State")
                st.json(current_state)
            
            with col2:
                st.subheader("Node Health")
                for node_id, metrics in current_state['node_health_metrics'].items():
                    st.write(f"**{node_id}**: CPU {metrics['cpu_usage']:.1f}%, Memory {metrics['memory_usage']:.1f}%, Error rate {metrics['error_rate']:.3f}")
        
        # Display metrics
        with metrics_placeholder.container():
            st.subheader("Simulation Metrics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Bandwidth Utilization", f"{st.session_state.metrics['bandwidth_utilization'][-1]:.2f}%")
                st.metric("Packet Loss", f"{st.session_state.metrics['packet_loss'][-1]:.3f}%")
                st.metric("Latency", f"{st.session_state.metrics['latency'][-1]:.1f}ms")
            
            with col2:
                st.metric("Threats Detected", st.session_state.metrics['threats_detected'])
                st.metric("Contracts Created", st.session_state.metrics['contracts_created'])
                st.metric("Contracts Terminated", st.session_state.metrics['contracts_terminated'])
            
            with col3:
                # Simple charts
                if len(st.session_state.metrics['bandwidth_utilization']) > 1:
                    st.line_chart(st.session_state.metrics['bandwidth_utilization'])
                    st.caption("Bandwidth Utilization Over Time")
        
        # Display threats
        with threats_placeholder.container():
            st.subheader("Detected Threats")
            if st.session_state.threats:
                for i, threat in enumerate(st.session_state.threats[-3:]):
                    with st.expander(f"Threat {i+1}: {threat['threat_data']['type']} - Probability: {threat['threat_data']['probability']:.2f}"):
                        st.json(threat)
        
        # Delay between cycles
        time.sleep(1 / simulation_speed)

# Main page layout
tab1, tab2, tab3 = st.tabs(["Simulation", "About HEIST", "AI Capabilities"])

with tab1:
    st.write("This dashboard allows you to visualize a simulated HEIST system with AI-powered threat detection.")
    
    if st.button("Run Simulation", type="primary"):
        run_simulation()

with tab2:
    st.markdown("""
    ## About HEIST
    
    The Hybrid Space/Submarine Architecture Ensuring Infosec of Telecommunications (HEIST) is an international consortium 
    aiming to enhance the security and resilience of global telecommunications infrastructure. 
    
    Given the increasing threats to subsea cables and the critical importance of secure data transfer, 
    HEIST proposes a hybrid architecture combining submarine surveillance, satellite communication, 
    and data rerouting mechanisms to safeguard information flow.
    
    ### Key Components:
    
    1. **Situational Awareness Hub**: Monitors infrastructure for threats and issues alerts
    2. **Routing Hub**: Dynamically routes traffic based on network conditions
    3. **Nodes**: Represent network elements like satellites and ground stations
    4. **Smart Contracts**: Secure the communication handshakes between nodes
    """)

with tab3:
    st.markdown("""
    ## AI Capabilities
    
    The HEIST system incorporates Azure OpenAI for advanced threat detection and analysis:
    
    ### Predictive Threat Detection
    
    - Real-time analysis of network telemetry data
    - Pattern recognition for early threat identification
    - Probability scoring of potential threats
    - Detailed threat characterization and classification
    
    ### Threat Resolution Prediction
    
    - Monitors ongoing threats for signs of resolution
    - Predicts when conditions are improving
    - Determines when to safely terminate emergency contracts
    
    ### Intelligent Network Monitoring
    
    - Analyzes bandwidth utilization patterns
    - Identifies abnormal network behavior
    - Monitors environmental factors like solar activity
    - Tracks node health metrics for predictive maintenance
    
    ### Benefits
    
    - Earlier detection of potential disruptions
    - More accurate threat assessment
    - Reduced false positives
    - Enhanced situational awareness
    - Improved decision-making for routing
    """)

# Add a footer
st.markdown("""
---
HEIST Simulation | Developed with 🛰️ | Using Azure OpenAI Services
""")