import streamlit as st
import json
import random
import time
from datetime import datetime, timedelta
import math

# This version is designed to run with ONLY streamlit as a dependency
# It doesn't attempt to use any other libraries to avoid deployment issues

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
    # New anomaly detection settings
    anomaly_sensitivity = st.slider("Anomaly Detection Sensitivity", 0.1, 1.0, 0.5, 0.1)
    forecast_horizon = st.slider("Forecast Horizon (hours)", 1, 24, 6)

# Helper function to get current timestamp as string
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Helper function to generate time series with anomalies
def generate_time_series_with_anomalies(length=24, anomaly_probability=0.15):
    """Generate a time series with occasional anomalies"""
    base_value = random.uniform(30, 70)
    time_series = []
    timestamps = []
    
    # Create timestamps for the past {length} hours
    current_time = datetime.now()
    for i in range(length):
        past_time = current_time - timedelta(hours=length-i)
        timestamps.append(past_time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Create the time series with normal pattern and occasional anomalies
    for i in range(length):
        # Normal pattern with slight variations and daily cycle
        hour_of_day = (current_time - timedelta(hours=length-i)).hour
        time_factor = math.sin(hour_of_day * math.pi / 12) * 10  # Daily cycle
        normal_value = base_value + time_factor + random.uniform(-5, 5)
        
        # Occasionally introduce anomalies
        if random.random() < anomaly_probability:
            # Sudden spike or drop
            anomaly_value = normal_value * random.choice([1.5, 1.7, 0.3, 0.5]) 
            time_series.append(anomaly_value)
        else:
            time_series.append(normal_value)
    
    return timestamps, time_series

# Anomaly detection simulation
def detect_anomalies(time_series, timestamps, sensitivity=0.5):
    """Simulate Azure Anomaly Detector on time series data"""
    anomalies = []
    for i in range(len(time_series)):
        # Use a simple algorithm to detect outliers
        # In a real implementation, this would call Azure Anomaly Detector API
        if i > 0 and i < len(time_series) - 1:
            prev_val = time_series[i-1]
            curr_val = time_series[i]
            next_val = time_series[i+1]
            
            # Detect sudden changes compared to neighbors
            avg_neighbors = (prev_val + next_val) / 2
            deviation = abs(curr_val - avg_neighbors) / avg_neighbors
            
            # Adjust threshold based on sensitivity
            threshold = 0.3 * (1 - sensitivity) + 0.1
            
            if deviation > threshold:
                anomalies.append({
                    "timestamp": timestamps[i],
                    "value": curr_val,
                    "expected_value": avg_neighbors,
                    "deviation": deviation,
                    "severity": "High" if deviation > threshold * 1.5 else "Medium"
                })
    
    return anomalies

# Generate natural language report for threats and anomalies
def generate_nlp_threat_report(threat_data, anomalies, forecast_data=None):
    """Generate a natural language report analyzing threats and anomalies"""
    if not threat_data and not anomalies:
        return "No significant threats or anomalies detected in the current analysis period."
    
    # Start with an executive summary
    report = "## HEIST Threat Intelligence Report\n\n"
    report += f"**Analysis Period:** {datetime.now() - timedelta(hours=24)} to {datetime.now()}\n\n"
    
    # Overall threat assessment
    if threat_data:
        threat_level = threat_data["threat_data"]["probability"]
        if threat_level > 0.7:
            assessment = "CRITICAL"
        elif threat_level > 0.5:
            assessment = "HIGH"
        elif threat_level > 0.3:
            assessment = "MODERATE"
        else:
            assessment = "LOW"
    else:
        assessment = "LOW"
        
    report += f"**Overall Threat Assessment: {assessment}**\n\n"
    
    # Executive Summary
    report += "### Executive Summary\n\n"
    
    if threat_data:
        report += f"Active threat detected: **{threat_data['threat_data']['type']}** with " + \
                 f"{threat_data['threat_data']['probability']:.1%} confidence level. "
        report += f"{threat_data['threat_data']['details']}\n\n"
    
    if anomalies:
        report += f"**{len(anomalies)}** anomalous network behavior patterns detected in the last 24 hours. "
        
        # Categorize anomalies
        high_severity = sum(1 for a in anomalies if a["severity"] == "High")
        if high_severity > 0:
            report += f"This includes {high_severity} high-severity anomalies that require immediate attention.\n\n"
        else:
            report += "None of these anomalies are currently classified as high severity.\n\n"
    
    # Detailed Threat Analysis
    if threat_data:
        report += "### Detailed Threat Analysis\n\n"
        report += f"The **{threat_data['threat_data']['type']}** threat was first detected at " + \
                 f"{threat_data['timestamp']}. Analysis of network telemetry indicates this may be "
        
        # Add specific analysis based on threat type
        threat_type = threat_data['threat_data']['type']
        if "Denial of Service" in threat_type:
            report += "a coordinated attempt to overwhelm system resources through multiple connection requests. "
            report += "The attack signature matches patterns observed in recent campaigns against critical infrastructure.\n\n"
        elif "Signal Jamming" in threat_type:
            report += "an intentional electromagnetic interference affecting satellite communications in sectors 3 and 4. "
            report += "The interference pattern suggests a sophisticated ground-based jamming system.\n\n"
        elif "Bandwidth Saturation" in threat_type:
            report += "an attempt to consume available bandwidth through numerous large data transfers. "
            report += "Traffic analysis shows unusual patterns consistent with data exfiltration attempts.\n\n"
        elif "Node Compromise" in threat_type:
            report += "an unauthorized access attempt targeting vulnerable nodes in the network. "
            report += "Several authentication anomalies have been detected suggesting credential theft or exploitation of known vulnerabilities.\n\n"
        else:
            report += "consistent with emerging threats identified in recent intelligence briefings. "
            report += "The threat shows characteristics of advanced persistent actors with significant resources.\n\n"
        
        # Affected systems
        report += "**Affected Systems:**\n\n"
        # Generate some fake affected systems based on the network state
        for i in range(1, random.randint(2, 4)):
            confidence = random.uniform(0.65, 0.95)
            report += f"- Node_{i}: {confidence:.1%} probability of compromise\n"
        report += "\n"
    
    # Anomaly Analysis
    if anomalies:
        report += "### Network Anomaly Analysis\n\n"
        report += f"{len(anomalies)} anomalies were detected using advanced time-series analysis. The most significant anomalies are:\n\n"
        
        # Sort anomalies by deviation (most significant first)
        sorted_anomalies = sorted(anomalies, key=lambda x: x["deviation"], reverse=True)
        
        # Report on top 3 anomalies
        for i, anomaly in enumerate(sorted_anomalies[:3]):
            report += f"**Anomaly {i+1}** - {anomaly['timestamp']}:\n"
            report += f"- Observed value: {anomaly['value']:.2f}\n"
            report += f"- Expected value: {anomaly['expected_value']:.2f}\n"
            report += f"- Deviation: {anomaly['deviation']:.1%}\n"
            report += f"- Severity: {anomaly['severity']}\n"
            
            # Add interpretation
            report += "- Interpretation: "
            if anomaly['value'] > anomaly['expected_value']:
                report += f"Sudden spike in network activity that exceeds expected patterns by {anomaly['deviation']:.1%}. "
                report += "This may indicate a sudden surge in legitimate traffic or the beginning of a resource exhaustion attack.\n\n"
            else:
                report += f"Unexpected drop in network activity, {abs(anomaly['deviation']):.1%} below expected values. "
                report += "This may indicate service disruption, node failure, or intentional communication blackout.\n\n"
    
    # Add forecast if available
    if forecast_data:
        report += "### Threat Forecast\n\n"
        report += f"Based on current trends, our AI models predict the following for the next {forecast_horizon} hours:\n\n"
        
        # Generate fake forecast data
        if threat_data and threat_data["threat_data"]["probability"] > 0.5:
            report += "- The current threat situation is expected to **escalate** in the next 4-6 hours\n"
            report += "- Probability of additional node compromise: 72%\n"
            report += "- Estimated time to network stability without intervention: 9.5 hours\n\n"
        else:
            report += "- No significant threats expected in the forecast window\n"
            report += "- Network stability forecast: 97.5% confidence\n"
            report += "- Recommendation: Continue routine monitoring\n\n"
    
    # Recommendations
    report += "### Recommended Actions\n\n"
    
    if threat_data and threat_data["threat_data"]["probability"] > 0.7:
        report += "**IMMEDIATE ACTION REQUIRED:**\n\n"
        report += "1. Activate emergency communication protocols\n"
        report += "2. Deploy countermeasures on affected nodes\n"
        report += "3. Implement traffic filtering at network boundaries\n"
        report += "4. Notify all connected satellite operators of the situation\n"
        report += "5. Begin incident response procedures according to protocol Alpha-7\n\n"
    elif threat_data and threat_data["threat_data"]["probability"] > 0.4:
        report += "**HIGH PRIORITY ACTIONS:**\n\n"
        report += "1. Increase monitoring of affected network segments\n"
        report += "2. Prepare backup communication channels\n"
        report += "3. Verify integrity of authentication systems\n"
        report += "4. Review recent configuration changes\n"
        report += "5. Alert on-call security team\n\n"
    else:
        report += "**STANDARD PROCEDURES:**\n\n"
        report += "1. Continue monitoring system with normal protocols\n"
        report += "2. Document anomalies in the security log\n"
        report += "3. Review firewall rules during next maintenance window\n"
        report += "4. No escalation required at this time\n\n"
    
    # Closing
    report += "---\n\n"
    report += "*This report was automatically generated by HEIST AI Threat Analysis Engine*\n"
    report += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return report

# Mock data generator functions
def generate_network_state():
    return {
        "timestamp": get_timestamp(),
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
    # Initialize state storage in session state
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
    if 'anomalies' not in st.session_state:
        st.session_state.anomalies = []
    
    # Generate time series data and detect anomalies
    timestamps, bandwidth_series = generate_time_series_with_anomalies(24)
    anomalies = detect_anomalies(bandwidth_series, timestamps, anomaly_sensitivity)
    st.session_state.anomalies = anomalies
    
    # Create placeholders for UI updates
    output_placeholder = st.empty()
    network_state_placeholder = st.empty()
    metrics_placeholder = st.empty()
    threats_placeholder = st.empty()
    anomaly_placeholder = st.empty()
    report_placeholder = st.empty()
    
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
        current_threat = None
        if threat_data:
            if threat_data["threat_data"]["probability"] > high_alert_threshold:
                st.session_state.metrics['threats_detected'] += 1
                st.session_state.metrics['contracts_created'] += 1
                st.session_state.threats.append(threat_data)
                current_threat = threat_data
            elif threat_data["threat_data"]["probability"] > medium_alert_threshold:
                st.session_state.threats.append(threat_data)
                current_threat = threat_data
        
        # Generate NLP report based on current threats and anomalies
        nlp_report = generate_nlp_threat_report(current_threat, anomalies, {"forecast_horizon": forecast_horizon})
        
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
        
        # Display anomaly detection
        with anomaly_placeholder.container():
            st.subheader("Anomaly Detection Results")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Create visualization data
                chart_data = {"timestamp": timestamps, "value": bandwidth_series, "is_anomaly": [0] * len(timestamps)}
                for anomaly in anomalies:
                    idx = timestamps.index(anomaly["timestamp"])
                    chart_data["is_anomaly"][idx] = anomaly["value"]
                
                # Plot the data
                bandwidth_data = {"Time": timestamps, "Bandwidth": bandwidth_series}
                
                st.line_chart(bandwidth_data)
                
                if anomalies:
                    anomaly_data = {
                        "Time": [a["timestamp"] for a in anomalies], 
                        "Value": [a["value"] for a in anomalies]
                    }
                    st.scatter_chart(anomaly_data)
                
            with col2:
                st.write(f"**Detected Anomalies:** {len(anomalies)}")
                st.write(f"Sensitivity: {anomaly_sensitivity:.2f}")
                st.write(f"Analysis Period: 24 hours")
                
                if anomalies:
                    with st.expander("Anomaly Details"):
                        for i, anomaly in enumerate(anomalies):
                            st.write(f"**Anomaly {i+1}**")
                            st.write(f"Time: {anomaly['timestamp']}")
                            st.write(f"Value: {anomaly['value']:.2f}")
                            st.write(f"Expected: {anomaly['expected_value']:.2f}")
                            st.write(f"Severity: {anomaly['severity']}")
                            st.write("---")
        
        # Display threats and NLP report
        with threats_placeholder.container():
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Detected Threats")
                if st.session_state.threats:
                    for i, threat in enumerate(st.session_state.threats[-3:]):
                        with st.expander(f"Threat {i+1}: {threat['threat_data']['type']} - Probability: {threat['threat_data']['probability']:.2f}"):
                            st.json(threat)
            
            with col2:
                st.subheader("AI Threat Analysis Report")
                with report_placeholder.container():
                    st.markdown(nlp_report)
        
        # Delay between cycles
        time.sleep(1 / simulation_speed)

# Main page layout with tabs
tab1, tab2, tab3, tab4 = st.tabs(["Simulation", "Anomaly Detection", "Threat Analysis", "About HEIST"])

with tab1:
    st.write("This dashboard allows you to visualize a simulated HEIST system with AI-powered threat detection.")
    
    if st.button("Run Simulation", type="primary"):
        run_simulation()

with tab2:
    st.markdown("""
    ## Azure Anomaly Detector Integration
    
    The HEIST system leverages Azure Anomaly Detector for advanced time-series analysis of network metrics. This provides:
    
    - **Real-time anomaly detection** on network bandwidth, latency, and error rates
    - **Multivariate analysis** to detect complex patterns across multiple metrics
    - **Seasonal pattern recognition** to differentiate between normal cyclical behavior and true anomalies
    - **Adaptive learning** that improves detection accuracy over time
    
    The system can detect subtle anomalies that might indicate early stages of:
    - Service degradation
    - Denial of service attacks
    - Resource exhaustion
    - Communication jamming
    - Node compromise

    Run the simulation to see anomaly detection in action.
    """)
    
    # Sample anomaly detection visual
    timestamps, bandwidth_series = generate_time_series_with_anomalies(24)
    anomalies = detect_anomalies(bandwidth_series, timestamps, 0.5)
    
    st.subheader("Sample Anomaly Detection")
    
    # Convert data to format for Streamlit charts
    sample_data = {"Time": timestamps, "Value": bandwidth_series}
    st.line_chart(sample_data)
    
    if anomalies:
        st.write(f"Detected {len(anomalies)} anomalies in sample data")
        anomaly_data = {
            "Time": [a["timestamp"] for a in anomalies], 
            "Value": [a["value"] for a in anomalies]
        }
        st.scatter_chart(anomaly_data)

with tab3:
    st.markdown("""
    ## Natural Language Threat Analysis
    
    HEIST incorporates advanced natural language processing to translate complex threat data into clear, actionable intelligence reports:
    
    - **Automatic report generation** that synthesizes data from multiple sources
    - **Severity classification** that accurately gauges threat levels
    - **Context-aware analysis** that considers historical patterns and known threats
    - **Actionable recommendations** tailored to the specific threat scenario
    
    Intelligence reports include:
    - Executive summary for quick situational awareness
    - Detailed threat analysis with technical specifics
    - Anomaly correlation and pattern recognition
    - Time-based forecasting of threat evolution
    - Prioritized action recommendations
    
    Run the simulation to generate a real-time threat intelligence report.
    """)
    
    # Sample threat report
    sample_threat = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "threat_data": {
            "type": "Signal Jamming",
            "probability": 0.78,
            "details": "Elevated packet loss rates and abnormal signal patterns detected across multiple nodes."
        }
    }
    
    sample_report = generate_nlp_threat_report(sample_threat, anomalies[:2], {"forecast_horizon": 6})
    
    with st.expander("View Sample Threat Intelligence Report"):
        st.markdown(sample_report)

with tab4:
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
    5. **AI Analysis**: Provides advanced threat detection and predictive capabilities
    
    ### AI Capabilities
    
    The HEIST system incorporates Azure OpenAI for advanced threat detection and analysis:
    
    #### Predictive Threat Detection
    
    - Real-time analysis of network telemetry data
    - Pattern recognition for early threat identification
    - Probability scoring of potential threats
    - Detailed threat characterization and classification
    
    #### Threat Resolution Prediction
    
    - Monitors ongoing threats for signs of resolution
    - Predicts when conditions are improving
    - Determines when to safely terminate emergency contracts
    
    #### Intelligent Network Monitoring
    
    - Analyzes bandwidth utilization patterns
    - Identifies abnormal network behavior
    - Monitors environmental factors like solar activity
    - Tracks node health metrics for predictive maintenance
    """)

# Add a footer
st.markdown("""
---
HEIST Simulation | Developed with 🛰️ | Using Azure OpenAI Services
""")