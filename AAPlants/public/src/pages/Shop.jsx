import React from 'react';
import PlantCard from './PlantCard';

const plants = [
    { name: 'Rose', description: 'A beautiful flowering plant.', image: '/images/rose.jpg' },
    { name: 'Cactus', description: 'A resilient desert plant.', image: '/images/cactus.jpg' },
    // Add more plants here...
];

const Shop = () => (
    <div className="shop-container">
        <div className="filter-sidebar">
            <h3>Filter by Category</h3>
            <ul>
                <li><input type="checkbox" /> Indoor</li>
                <li><input type="checkbox" /> Outdoor</li>
                <li><input type="checkbox" /> Flowering</li>
                <li><input type="checkbox" /> Low Light</li>
            </ul>
        </div>
        <div className="plant-grid">
            {plants.map((plant, index) => (
                <PlantCard key={index} plant={plant} />
            ))}
        </div>
    </div>
);

export default Shop;
