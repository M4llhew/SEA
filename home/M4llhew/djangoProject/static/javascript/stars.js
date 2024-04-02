const numStars = 175; // Adjust the number of stars as needed
const container = document.getElementById("stars-container");
const starsPerInterval = 10; // Number of stars to create per interval

// Define the probabilities for each star type
const probabilities = {
    "star-type-1": 0.6, // 60% probability for star-type-1
    "star-type-2": 0.3, // 30% probability for star-type-2
    "star-type-3": 0.1, // 10% probability for star-type-3
};

// Array of star classes based on the probabilities
const starClasses = [];
for (const starClass in probabilities) {
    const probability = probabilities[starClass];
    const numStarsOfType = Math.round(numStars * probability);
    starClasses.push(...Array(numStarsOfType).fill(starClass));
}

// Shuffle the star classes array to randomize star types
shuffleArray(starClasses);

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function createStar() {
    const star = document.createElement("div");

    // Randomly select a star class from the shuffled array
    const randomStarClass = starClasses[Math.floor(Math.random() * starClasses.length)];
    star.className = randomStarClass;

    // Randomly set the position of the star within the container
    star.style.left = `${Math.random() * 100}%`;
    star.style.top = `${Math.random() * 100}%`;

    container.appendChild(star);

    // Remove stars that have moved beyond the top of the container
    star.addEventListener("animationiteration", () => {
        container.removeChild(star);
    });
}

// Create the initial stars with random positions
for (let i = 0; i < numStars; i++) {
    createStar();
}

// Continuously spawn stars at a regular interval
setInterval(() => {
    for (let i = 0; i < starsPerInterval; i++) {
        createStar();
    }
}, 1000);