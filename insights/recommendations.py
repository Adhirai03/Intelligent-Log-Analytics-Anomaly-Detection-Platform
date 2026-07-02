EVENT_INFO = {

"E1": {
    "title": "Duplicate Block",
    "cause": "The system attempted to create a block that already exists.",
    "recommendation": "Check for duplicate write requests or repeated client operations.",
    "risk": "Low"
},

"E2": {
    "title": "Verification Successful",
    "cause": "Normal block verification completed successfully.",
    "recommendation": "No action required.",
    "risk": "None"
},

"E3": {
    "title": "Block Served",
    "cause": "A client successfully received a requested block.",
    "recommendation": "Normal filesystem activity.",
    "risk": "None"
},

"E4": {
    "title": "Serving Exception",
    "cause": "The DataNode encountered an exception while serving a block.",
    "recommendation": "Inspect DataNode logs and verify disk and network health.",
    "risk": "Medium"
},

"E5": {
    "title": "Receiving Block",
    "cause": "A DataNode is receiving a block from another node.",
    "recommendation": "Normal replication activity unless unusually frequent.",
    "risk": "Low"
},

"E6": {
    "title": "Block Received",
    "cause": "A block transfer completed successfully.",
    "recommendation": "No action required.",
    "risk": "None"
},

"E7": {
    "title": "Write Exception",
    "cause": "An exception occurred while writing a block.",
    "recommendation": "Check storage availability and disk permissions.",
    "risk": "High"
},

"E8": {
    "title": "Packet Interrupted",
    "cause": "Data packet transmission was interrupted.",
    "recommendation": "Investigate network stability and node availability.",
    "risk": "Medium"
},

"E9": {
    "title": "Receiving Block Packet",
    "cause": "The DataNode is receiving packets of block data.",
    "recommendation": "Normal communication event.",
    "risk": "None"
},

"E10": {
    "title": "PacketResponder Exception",
    "cause": "PacketResponder encountered an unexpected exception.",
    "recommendation": "Check DataNode health and network latency.",
    "risk": "High"
},

"E11": {
    "title": "PacketResponder Terminated",
    "cause": "PacketResponder process terminated unexpectedly.",
    "recommendation": "Restart affected DataNode and inspect error logs.",
    "risk": "High"
},

"E12": {
    "title": "Mirror Write Exception",
    "cause": "Writing replicated data to another node failed.",
    "recommendation": "Verify replica node connectivity.",
    "risk": "High"
},

"E13": {
    "title": "Empty Packet",
    "cause": "The DataNode received an empty packet.",
    "recommendation": "Monitor for communication inconsistencies.",
    "risk": "Low"
},

"E14": {
    "title": "ReceiveBlock Exception",
    "cause": "The DataNode failed while receiving block data.",
    "recommendation": "Inspect storage hardware and network communication.",
    "risk": "High"
},

"E15": {
    "title": "Metadata Offset Change",
    "cause": "Block metadata offsets were updated.",
    "recommendation": "Normal metadata maintenance activity.",
    "risk": "Low"
},

"E16": {
    "title": "Block Transmitted",
    "cause": "A block was successfully transmitted.",
    "recommendation": "No action required.",
    "risk": "None"
},

"E17": {
    "title": "Transfer Failed",
    "cause": "The system failed to transfer a block.",
    "recommendation": "Check network connectivity and destination node health.",
    "risk": "High"
},

"E18": {
    "title": "Transfer Started",
    "cause": "A block transfer operation has started.",
    "recommendation": "Normal replication event.",
    "risk": "Low"
},

"E19": {
    "title": "Block Reopened",
    "cause": "A block was reopened after a previous operation.",
    "recommendation": "Monitor repeated reopen events for application issues.",
    "risk": "Medium"
},

"E20": {
    "title": "Block Delete Error",
    "cause": "The system attempted to delete a block that could not be located.",
    "recommendation": "Verify filesystem consistency and metadata integrity.",
    "risk": "Medium"
},

"E21": {
    "title": "Block Deleted",
    "cause": "A block file was deleted.",
    "recommendation": "Normal filesystem maintenance.",
    "risk": "Low"
},

"E22": {
    "title": "Allocate Block",
    "cause": "The NameNode allocated a new block.",
    "recommendation": "Normal filesystem allocation.",
    "risk": "None"
},

"E23": {
    "title": "Invalid Block",
    "cause": "The NameNode marked a block as invalid.",
    "recommendation": "Investigate possible metadata corruption.",
    "risk": "High"
},

"E24": {
    "title": "Replication Cleanup",
    "cause": "The system removed unnecessary replication information.",
    "recommendation": "Normal replication maintenance.",
    "risk": "Low"
},

"E25": {
    "title": "Replication Requested",
    "cause": "Replication of a block has been requested.",
    "recommendation": "Monitor replication progress.",
    "risk": "Low"
},

"E26": {
    "title": "Stored Block Updated",
    "cause": "Metadata for a stored block was updated.",
    "recommendation": "Repeated updates may indicate unstable block placement. Check NameNode logs.",
    "risk": "Medium"
},

"E27": {
    "title": "Redundant Replica",
    "cause": "The NameNode received a redundant replica report.",
    "recommendation": "Verify replication factor configuration.",
    "risk": "Medium"
},

"E28": {
    "title": "Invalid Stored Block",
    "cause": "A stored block does not belong to any known file.",
    "recommendation": "Inspect filesystem metadata and recover orphaned blocks.",
    "risk": "Critical"
},

"E29": {
    "title": "Replication Timeout",
    "cause": "Replication monitor timed out while waiting for block replication.",
    "recommendation": "Check overloaded DataNodes and network congestion.",
    "risk": "High"
}

}

from explainability.shap_analysis import get_top_features


def build_ai_insight(row):

    top = get_top_features(row)

    report = []

    highest = "None"

    order = {
        "None":0,
        "Low":1,
        "Medium":2,
        "High":3,
        "Critical":4
    }

    for _, r in top.iterrows():

        event = r["Feature"]

        info = EVENT_INFO[event]

        if order[info["risk"]] > order[highest]:
            highest = info["risk"]

        report.append(info)

    return {

        "risk": highest,
        "events": report

    }