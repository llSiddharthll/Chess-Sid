// Function to toggle theme
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute("data-theme");
  const newTheme = currentTheme === "light" ? "dark" : "light";

  // Set the new theme in the HTML attribute
  document.documentElement.setAttribute("data-theme", newTheme);

  // Save the theme preference in localStorage
  localStorage.setItem("theme", newTheme);
  document.documentElement.classList.add("theme-transition"); // Add a transition class

    setTimeout(() => {
        document.documentElement.classList.remove("theme-transition"); // Remove it after a delay
    }, 100); // Adjust delay as needed
}

// Function to set the theme based on user preference in localStorage
function setTheme() {
  console.log("setTheme function called");
  const savedTheme = localStorage.getItem("theme");

  // Set the theme from localStorage, or default to light if not available
  document.documentElement.setAttribute("data-theme", savedTheme || "light");
}

// Set the theme on page load
window.onload = setTheme;