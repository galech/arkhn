import {Deployment} from "../types";
import React from "react";

interface Props {
    deployment: Deployment,
    deleteDeployment: () => void,
    style?: React.CSSProperties,
    updateDeployment?: () => void
}

export default function DeploymentItem({deployment, deleteDeployment, style, updateDeployment}: Props) {
    return (
        <div style={style}>
            <div style={{flex: 3}}>{deployment.label}</div>
            <div style={{flex: 3}}>{deployment.image}</div>
            <div style={{flex: 2}}>{deployment.replicas}</div>
            <div style={{flex: 1, textAlign: "right"}}>
                <button onClick={updateDeployment}>Edit</button>
                <button onClick={deleteDeployment}>Supprimer</button>
            </div>
        </div>
    );
}
