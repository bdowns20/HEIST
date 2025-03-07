import streamlit as st
import time
import random
import os
import json
import sys
from dotenv import load_dotenv

# Handle potential missing dependencies gracefully
try:
    from node import Node
    from data_request import DataRequest
    from routing_hub import RoutingHub
    from utility_functions import detect_disruption
    from situational_awareness_hub import SituationalAwarenessHub
except ImportError as e:
    st.error(f"Error importing dependencies: {e}")
    st.info("Please install required packages using: pip install -r requirements.txt")
    # Continue with mock implementations instead of exiting

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="HEIST Simulation",
    page_icon="🛰️",
    layout="wide"
)

st.title("HEIST Simulation Dashboard")
st.subheader("Hybrid Space/Submarine Architecture Ensuring Infosec of Telecommunications")

# Sidebar for configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Azure API Key", os.environ.get("AZURE_API_KEY", ""), type="password")
api_endpoint = st.sidebar.text_input("Azure Endpoint", os.environ.get("AZURE_ENDPOINT", ""))

# Update environment variables if changed
if api_key and api_key != os.environ.get("AZURE_API_KEY", ""):
    os.environ["AZURE_API_KEY"] = api_key
if api_endpoint and api_endpoint != os.environ.get("AZURE_ENDPOINT", ""):
    os.environ["AZURE_ENDPOINT"] = api_endpoint

# Simulation parameters
num_cycles = st.sidebar.slider("Simulation Cycles", 1, 20, 5)
simulation_speed = st.sidebar.slider("Simulation Speed", 0.1, 2.0, 1.0)
advanced_options = st.sidebar.expander("Advanced Options")

with advanced_options:
    high_alert_threshold = st.slider("High Alert Threshold", 0.5, 0.9, 0.7, 0.05)
    medium_alert_threshold = st.slider("Medium Alert Threshold", 0.2, 0.6, 0.4, 0.05)
    threat_randomness = st.slider("Threat Randomness", 0.1, 1.0, 0.5, 0.1)

# Mock blockchain setup (since we can't connect to Ganache without setup)
class MockWeb3:
    class MockEth:
        def __init__(self):
            self.accounts = [
                f"0x{i}123456789abcdef0123456789abcdef01234567" for i in range(1, 7)
            ]
    
    def __init__(self):
        self.eth = self.MockEth()
        self.middleware_onion = type('obj', (object,), {
            'inject': lambda *args, **kwargs: None
        })

class MockContract:
    def __init__(self):
        self.functions = self
    
    def createHandshake(self, *args):
        return self
    
    def terminateHandshake(self, *args):
        return self
    
    def call(self, *args, **kwargs):
        return random.randint(1000, 9999)
    
    def transact(self, *args, **kwargs):
        return {'transactionHash': f"0x{random.randint(10000, 99999)}"}

def run_simulation():
    # Create placeholder for simulation output
    output_placeholder = st.empty()
    network_state_placeholder = st.empty()
    metrics_placeholder = st.empty()
    threats_placeholder = st.empty()
    
    # Initialize state
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
    
    # Setup mock environment
    w3 = MockWeb3()
    mock_contract = MockContract()
    
    # Initialize nodes
    nodes = []
    for i in range(2, 7):
        node = Node(
            node_id=i-1,
            bandwidth=random.randint(1000, 2500),
            w3=w3,
            contract=mock_contract,
            account=w3.eth.accounts[i-2],
            private_key=f"0x{i}abcdef1234567890abcdef1234567890abcdef"
        )
        nodes.append(node)
    
    # Create hubs
    routing_hub = RoutingHub(
        nodes=nodes, 
        w3=w3, 
        contract=mock_contract,
        requester_account=w3.eth.accounts[0],
        requester_private_key="0x1abcdef1234567890abcdef1234567890abcdef"
    )
    
    # Create SA Hub with custom thresholds
    sa_hub = SituationalAwarenessHub()
    sa_hub.high_alert_threshold = high_alert_threshold
    sa_hub.medium_alert_threshold = medium_alert_threshold
    
    # Generate random data requests
    data_requests = [
        DataRequest(
            request_id=i,
            source=f"GroundStation{random.randint(1,3)}",
            destination=f"Satellite{random.randint(1,3)}",
            data_size=random.choice([50, 100, 200]),
            importance=random.randint(1, 5),
            time_sensitivity=random.choice(["urgent", "normal", "no urgency"]),
            security_level=random.randint(1, 3),
            urgency=random.randint(1, 3),
            modulation=random.choice(["BPSK", "QPSK", "8-QAM", "16-QAM"]),
            datarate=random.choice(["0-10mbps", "10-100mbps", ">100mbps"]),
            latency_tolerance=random.choice(["<600ms", "<300ms", "<150ms"]),
            coverage_area=random.choice(["SISO", "SIMO", "MIMO"]),
            encryption=random.choice(["AES/GCM-128", "AES/GCM-256", "CARIBOU/CARDHOLDER"]),
            scheduling=random.choice(["No Urgency (<3 hours)", "Urgent (<30 mins)", "Continuous link"])
        ) for i in range(1, 11)
    ]
    
    # Capture print outputs
    import io
    import sys
    from contextlib import redirect_stdout
    
    # Run simulation cycles
    for cycle in range(1, num_cycles + 1):
        # Capture stdout
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            # Cycle header
            print(f"\n=== Simulation Cycle {cycle} ===")
            
            # Step 1: The SA Hub checks infrastructure
            sa_hub.monitor_infrastructure()
            
            # Log the current network state for display
            current_state = sa_hub.current_network_state
            
            # If a new threat is detected, issue alerts and route a request
            if sa_hub.alert_issued:
                sa_hub.issue_alerts(nodes)
                req = random.choice(data_requests)
                routing_hub.route_request(req)
                st.session_state.metrics['contracts_created'] += 1
            
            # If conditions are restored, terminate contracts
            if sa_hub.restored:
                active_contract_ids = list(routing_hub.active_contracts.keys())
                for cid in active_contract_ids:
                    routing_hub.terminate_contract(cid)
                st.session_state.metrics['contracts_terminated'] += len(active_contract_ids)
                sa_hub.reset_restored_flag()
            
            # Update nodes and process
            for node in nodes:
                node.update_environment_conditions()
            routing_hub.process_all_nodes()
            
            # Random new request
            if random.random() < 0.75:
                req = random.choice(data_requests)
                routing_hub.route_request(req)
                st.session_state.metrics['contracts_created'] += 1
            
            # Log high security contracts
            for cinfo in routing_hub.active_contracts.values():
                contract = cinfo['contract']
                routing_hub.log_high_classification_traffic(contract)
            
            # Run disruption detection
            detect_disruption(nodes, routing_hub)
        
        # Get the captured output
        output = captured_output.getvalue()
        
        # Update session state
        st.session_state.logs.append(output)
        
        # Update metrics
        if current_state:
            st.session_state.metrics['bandwidth_utilization'].append(current_state.get('bandwidth_utilization', 0))
            st.session_state.metrics['packet_loss'].append(current_state.get('packet_loss_rate', 0))
            st.session_state.metrics['latency'].append(current_state.get('latency_ms', 0))
            
            # Check if this was a threat cycle
            if "AI predicted threat" in output or "Threat detected" in output:
                st.session_state.metrics['threats_detected'] += 1
                
                # Extract threat info if available
                if hasattr(sa_hub, 'threat_history') and sa_hub.threat_history:
                    latest_threat = sa_hub.threat_history[-1]
                    st.session_state.threats.append(latest_threat)
        
        # Update UI
        # Display the full log
        output_placeholder.text_area("Simulation Log", "\n".join(st.session_state.logs[-5:]), height=300)
        
        # Display current network state
        with network_state_placeholder.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Current Network State")
                if current_state:
                    st.json(current_state)
            
            with col2:
                st.subheader("Node Health")
                if current_state and 'node_health_metrics' in current_state:
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
                    with st.expander(f"Threat {i+1}: {threat.get('threat_data', {}).get('type', 'Unknown')} - {threat.get('timestamp', 'Unknown time')}"):
                        st.json(threat)
        
        # Delay between cycles
        time.sleep(1 / simulation_speed)

# Main page layout
tab1, tab2, tab3 = st.tabs(["Simulation", "About HEIST", "AI Capabilities"])

with tab1:
    st.write("This dashboard allows you to run and visualize the HEIST simulation with AI-powered threat detection.")
    
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
    
    The HEIST system now incorporates Azure OpenAI for advanced threat detection and analysis:
    
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