# Python Distributed File Middleware

A distributed file middleware built in Python for a Distributed Systems course, implementing transparent file storage, replication and communication between clients, middleware and storage nodes using TCP sockets.

## Overview

This project simulates a distributed storage system composed of:

* A client application
* A middleware manager
* Multiple storage nodes

The middleware acts as an intermediary layer responsible for:

* File upload coordination
* File download routing
* Replication management
* Storage transparency
* File registry management

The client does not know where files are physically stored or replicated, providing abstraction and storage transparency.

## Architecture

```text
Client
   |
   v
Manager (Middleware)
   |
   +---- Storage 5001
   +---- Storage 5002
   +---- Storage 5003
   +---- Storage 5004
```

### Components

#### Client

Responsible for interacting with the user through a command-line interface.

Supported operations:

* Upload files
* Download files
* List uploaded files
* Exit application

#### Manager (Middleware)

Acts as the central coordinator between clients and storage nodes.

Responsibilities:

* Selecting storage nodes
* Managing replication
* Maintaining file registry metadata
* Routing download requests
* Providing storage transparency

The manager alternates storage allocation between nodes and automatically creates replicated copies.

#### Storage Nodes

Storage servers responsible for:

* Storing uploaded files
* Sending files during download requests
* Replicating files between nodes

Each storage node communicates using TCP sockets.

## Replication Strategy

The system maintains replicated copies of uploaded files.

Storage pairs:

* Storage 0 ↔ Storage 2
* Storage 1 ↔ Storage 3

When a file is uploaded:

1. The manager selects a primary storage node
2. A replica node is automatically selected
3. The storage node replicates the file to its paired node

This replication process is transparent to the client.

## Communication

All communication is implemented using:

* TCP sockets
* Python socket programming
* Buffered file transfer (4096-byte chunks)

Communication occurs between:

* Client ↔ Middleware
* Middleware ↔ Storage
* Storage ↔ Storage

## Features

* Distributed file upload
* File replication
* Transparent storage abstraction
* Distributed download routing
* File registry management
* Multi-node storage architecture
* TCP-based communication

## Technologies

* Python
* TCP Sockets
* Distributed Systems concepts
* Network Programming
* Client-Server Architecture

## Running the Project

### Start the Manager

In a separate terminal run:
```bash
python3 gerenciador.py
```

### Start Storage Nodes

In four different terminals run the following commands:
```bash
python3 storage.py 5001
python3 storage.py 5002
python3 storage.py 5003
python3 storage.py 5004
```

### Start Client

And at our last terminal run the client interface to run, inside the repo there are 2 different files you can test it, an image in .jpg and an .mp3 music.
```bash
python3 client.py
```

## Client Operations

### Upload

Uploads a file to the distributed storage system.

### Download

Downloads a file from the distributed storage system.

### List Uploads

Lists all uploaded files available in the cloud storage.

### Exit

Closes the client application.

## What I Learned

This project helped me explore several distributed systems concepts, including:

* Middleware architecture
* File replication
* Distributed storage transparency
* TCP network communication
* Client-server coordination
* Node communication
* File transfer protocols
* Distributed system organization

## Future Improvements

Possible future enhancements:

* Fault tolerance
* Leader election
* Heartbeat monitoring
* Dynamic node discovery
* Consistent hashing
* Concurrent client handling
* Encryption and authentication
* Containerization with Docker

## Academic Context

Developed for a Distributed Systems course during my Computer Science degree.
