package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

// Global variables for environment values
var (
	message      string
	location     string
	countryA2    string
	deploymentID string
	nodeID       string
	placementID  string
	region       string
)

func main() {
	// Set up logging with timestamp
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	log.Println("=== Go Container Starting ===")

	// Collect environment variables
	message = getEnvWithDefault("MESSAGE", "Hello, World!")
	location = getEnvWithDefault("CLOUDFLARE_LOCATION", "Unknown")
	countryA2 = getEnvWithDefault("CLOUDFLARE_COUNTRY_A2", "Unknown")
	deploymentID = getEnvWithDefault("CLOUDFLARE_DEPLOYMENT_ID", "Unknown")
	nodeID = getEnvWithDefault("CLOUDFLARE_NODE_ID", "Unknown")
	placementID = getEnvWithDefault("CLOUDFLARE_PLACEMENT_ID", "Unknown")
	region = getEnvWithDefault("CLOUDFLARE_REGION", "Unknown")

	// Set up HTTP server
	http.HandleFunc("/", handleRoot)

	port := getEnvWithDefault("PORT", "8080")
	log.Printf("Starting HTTP server on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
	log.Printf("Request received: %s %s", r.Method, r.URL.Path)

	// Log startup information
	log.Printf("Container started at: %s", time.Now().UTC().Format(time.RFC3339))
	log.Printf("Go version: %s", getGoVersion())
	log.Printf("Working directory: %s", getCurrentDir())

	// Log all collected environment variables
	log.Println("=== Environment Variables ===")
	log.Printf("MESSAGE: %s", message)
	log.Printf("CLOUDFLARE_LOCATION: %s", location)
	log.Printf("CLOUDFLARE_COUNTRY_A2: %s", countryA2)
	log.Printf("CLOUDFLARE_DEPLOYMENT_ID: %s", deploymentID)
	log.Printf("CLOUDFLARE_NODE_ID: %s", nodeID)
	log.Printf("CLOUDFLARE_PLACEMENT_ID: %s", placementID)
	log.Printf("CLOUDFLARE_REGION: %s", region)

	// Log additional system information
	log.Println("=== System Information ===")
	log.Printf("Hostname: %s", getHostname())
	log.Printf("Process ID: %d", os.Getpid())
	log.Printf("User ID: %d", os.Getuid())

	log.Println("=== Container initialization complete ===")

	// Return JSON response
	response := map[string]interface{}{
		"Message":                  message,
		"Cloudflare Location":      location,
		"Cloudflare Country":       countryA2,
		"Cloudflare Deployment ID": deploymentID,
		"Cloudflare Node ID":       nodeID,
		"Cloudflare Placement ID":  placementID,
		"Cloudflare Region":        region,
		"Container Started At":     time.Now().UTC().Format(time.RFC3339),
		"Go Version":               getGoVersion(),
		"Working Directory":        getCurrentDir(),
		"Hostname":                 getHostname(),
		"Process ID":               os.Getpid(),
		"User ID":                  os.Getuid(),
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// Helper function to get environment variable with default value
func getEnvWithDefault(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

// Get Go version information
func getGoVersion() string {
	return fmt.Sprintf("%s %s/%s",
		os.Getenv("GOLANG_VERSION"),
		os.Getenv("GOOS"),
		os.Getenv("GOARCH"))
}

// Get current working directory
func getCurrentDir() string {
	dir, err := os.Getwd()
	if err != nil {
		return "unknown"
	}
	return dir
}

// Get hostname
func getHostname() string {
	hostname, err := os.Hostname()
	if err != nil {
		return "unknown"
	}
	return hostname
}
