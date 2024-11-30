import React from 'react';
import './PlantCard.css';

const PlantCard = ({ plant }) => (
    <div className="plant-card">
        <img src={plant.image} alt={plant.name} />
        <h3>{plant.name}</h3>
        <p>{plant.description}</p>
        <button>View Details</button>
    </div>
);

export default PlantCard;
