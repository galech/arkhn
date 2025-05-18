import { useState, FormEvent } from "react";
import { Deployment } from "../types";

interface Props {
  deployment?: Deployment;  // si viene, es edición
  onCreated: (deployment: Deployment) => void;
  onUpdated: (deployment: Deployment) => void;
}

export default function DeploymentForm({ deployment, onCreated, onUpdated }: Props) {
  const [model, setModel] = useState(() => new Deployment(deployment));
  const handleChange = (field: keyof Deployment) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setModel((prev) => new Deployment({ ...prev, [field]: e.target.value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await model.save();
      model.id ? onUpdated(model) : onCreated(model);
    } catch (err) {
      console.error("Erreur lors de la sauvegarde", err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={model.label}
        onChange={handleChange("label")}
        placeholder="Nom du déploiement"
      />
      <input
        value={model.image}
        onChange={handleChange("image")}
        placeholder="Image"
      />
      <input
        type="number"
        value={model.replicas}
        onChange={(e) => setModel((prev) => new Deployment({ ...prev, replicas: Number(e.target.value) }))}
        placeholder="Nombre de réplicas"
      />
      <button type="submit">{model.id ? "Mettre à jour" : "Déployer"}</button>
    </form>
  );
}