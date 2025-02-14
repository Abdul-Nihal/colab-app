# Real-time Collaborative Editor

This application provides a real-time collaborative editing experience, Multiple users can edit the same CODE simultaneously, with changes reflected instantly for all participants.

## Getting Started

### Prerequisites

* Docker and Docker Compose (recommended) or a local installation of the application's dependencies.

### Running with Docker

1. **Clone the repository:**

   git clone https://github.com/Abdul-Nihal/colab-app.git
   cd colab-app
   
2.**Build and run the Docker container:**

  docker build -t colab-app-v1 .

  docker run -p 5000:5000 colab-app-v1
  
3.**Access the editor:**

 Open two browser windows (or tabs) and navigate to 
 http://localhost:5000 
 in each.

4.**Start collaborating:**

  Any text entered in one browser window will immediately appear in the other, demonstrating the real-time collaborative editing functionality.
  
