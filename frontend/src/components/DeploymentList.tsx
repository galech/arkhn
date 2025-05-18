import {useCallback, useEffect, useRef, useState} from "react";

import type {ListOnScrollProps} from "react-window"; // solo tipo, no valor en runtime
import {FixedSizeList as List} from "react-window";
import {Deployment} from "../types";
import DeploymentItem from "./DeploymentItem";
import Modal from "react-modal";
import DeploymentForm from "./DeploymentForm.tsx";

export default function DeploymentList() {


    const [listHeight, setListHeight] = useState(0);
    const [deploymentToEdit, setDeploymentToEdit] = useState<Deployment | null>(null);
    const [deployments, setDeployments] = useState<Deployment[]>([]);
    const [nextCursor, setNextCursor] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const listRef = useRef<List>(null);
    const listContainer = useRef<HTMLSpanElement>(null);
    const headerRef = useRef<HTMLHeadingElement>(null);

    const closeModal = () => {
        setDeploymentToEdit(null);
    };
    const genNewDeployment = () => {
        setDeploymentToEdit(new Deployment())
    }

    const fetchData = async (cursor?: string, append = false) => {
        setLoading(true);
        const deploymentListResponse = await Deployment.fetch(cursor);
        if (append) {
            setDeployments((prev) => [...prev, ...deploymentListResponse.deployments]);
        } else {
            setDeployments(deploymentListResponse.deployments);
        }
        setNextCursor(deploymentListResponse.cursor);
        setLoading(false);
    };

    const checkIfLoadMoreNeeded = () => {
        if (!listRef.current || loading || !nextCursor) return;
        const clientHeight = listRef.current.props.height;
        const contentHeight = deployments.length * listRef.current.props.itemSize;
        if (contentHeight < clientHeight) {
            fetchData(nextCursor, true)
        }
    };

    useEffect(() => {
        function updateHeight() {
            const headerHeight = headerRef.current?.offsetHeight ?? 0;
            const rect = listContainer.current.getBoundingClientRect();
            setListHeight(window.innerHeight - rect.top);
        }

        updateHeight();
        window.addEventListener("resize", updateHeight);
        return () => window.removeEventListener("resize", updateHeight);
    }, []);

    useEffect(() => {
        fetchData();
    }, []);

    useEffect(() => {
        checkIfLoadMoreNeeded();
    }, [deployments, nextCursor]);

    const handleScroll = useCallback((props: ListOnScrollProps) => {
        const {scrollOffset, scrollUpdateWasRequested, scrollDirection} = props;
        if (
            listRef.current &&
            !scrollUpdateWasRequested &&
            scrollDirection === "forward" &&
            nextCursor &&
            scrollOffset + listHeight >= (deployments.length * listRef.current.props.itemSize) - 100 &&
            !loading
        ) {
            fetchData(nextCursor, true);
        }
    }, [nextCursor, loading]);

    const Row = ({index, style}: { index: number; style: React.CSSProperties }) => {
        const deployment = deployments[index];
        const backgroundColor = index % 2 === 0 ? "#fff" : "#f0f0f0";
        return (
            <DeploymentItem
                deployment={deployment}
                style={{
                    ...style,
                    display: "flex",
                    backgroundColor,
                    padding: "0 10px",
                    alignItems: "center",
                    boxSizing: "border-box",
                }}
                deleteDeployment={() => {
                    deployment.delete()
                    setDeployments((prevDeployments) =>
                        prevDeployments.filter((d) => d.id !== deployment.id)
                    );
                }}
                updateDeployment={() => setDeploymentToEdit(deployment)}
            />

        );
    };

    return (
        <div>
            <h2 ref={headerRef} style={{margin: 0, padding: "1rem", textAlign: "center"}}>
                Deployment <button onClick={genNewDeployment}>New</button>
            </h2>
            <span ref={listContainer}>
            <List
                height={listHeight}
                itemCount={deployments.length}
                itemSize={50}
                width="100%"
                onScroll={handleScroll}
                ref={listRef}
            >
              {Row}
            </List>
      </span>

            <Modal isOpen={deploymentToEdit} onRequestClose={closeModal} contentLabel="Modal">
                <h2>{deploymentToEdit && deploymentToEdit.id ? "Update deployment" : "Create deployment"}</h2>
                <DeploymentForm
                    deployment={deploymentToEdit}
                    onCreated={(deployment) => {
                        setDeployments((prev) => [...prev, deployment]); // TODO
                        closeModal();
                    }}
                    onUpdated={(updatedDeployment) => {
                        setDeployments((prevDeployments) =>
                            prevDeployments.map((deployment) =>
                                deployment.id === updatedDeployment.id ? updatedDeployment : deployment
                            )
                        );
                        closeModal();
                    }}></DeploymentForm>
            </Modal>

        </div>
    );
}
