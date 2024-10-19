#include <stdio.h>
#include <stdlib.h>

#define MAX_NODES 100

// Structure to represent a queue
typedef struct {
    int items[MAX_NODES];
    int front, rear;
} Queue;

// Function to create a queue
Queue* createQueue() {
    Queue* q = (Queue*)malloc(sizeof(Queue));
    q->front = -1;
    q->rear = -1;
    return q;
}

// Function to check if the queue is empty
int isEmpty(Queue* q) {
    return q->front == -1;
}

// Function to add an element to the queue
void enqueue(Queue* q, int value) {
    if (q->rear == MAX_NODES - 1) {
        printf("Queue is full\n");
    } else {
        if (q->front == -1) {
            q->front = 0;
        }
        q->rear++;
        q->items[q->rear] = value;
    }
}

// Function to remove an element from the queue
int dequeue(Queue* q) {
    if (isEmpty(q)) {
        printf("Queue is empty\n");
        return -1;
    } else {
        int item = q->items[q->front];
        if (q->front >= q->rear) {
            q->front = q->rear = -1; // Reset queue
        } else {
            q->front++;
        }
        return item;
    }
}

// Function to perform BFS and search for a specific node
int bfs(int graph[MAX_NODES][MAX_NODES], int start, int target, int num_nodes) {
    int visited[MAX_NODES] = {0}; // Array to track visited nodes
    Queue* q = createQueue();     // Create the queue

    // Start from the initial node
    visited[start] = 1;           // Mark it as visited
    enqueue(q, start);            // Enqueue the starting node

    printf("BFS Traversal: ");

    while (!isEmpty(q)) {
        int current = dequeue(q);  // Dequeue a vertex
        printf("%d ", current);     // Print it

        // Check if we found the target node
        if (current == target) {
            printf("\nNode %d found!\n", target);
            return 1; // Node found
        }

        // Explore all adjacent nodes
        for (int i = 0; i < num_nodes; i++) {
            if (graph[current][i] == 1 && !visited[i]) { // If there's an edge and not visited
                visited[i] = 1;        // Mark it as visited
                enqueue(q, i);         // Enqueue the adjacent node
            }
        }
    }
    
    printf("\nNode %d not found.\n", target);
    return 0; // Node not found
}

// Main function
int main() {
    // Example graph represented as an adjacency matrix
    int graph[MAX_NODES][MAX_NODES] = {0};
    int num_nodes = 7;

    // Adding edges
    graph[0][1] = graph[1][0] = 1; // Edge between 0 and 1
    graph[0][2] = graph[2][0] = 1; // Edge between 0 and 2
    graph[1][3] = graph[3][1] = 1; // Edge between 1 and 3
    graph[1][4] = graph[4][1] = 1; // Edge between 1 and 4
    graph[2][5] = graph[5][2] = 1; // Edge between 2 and 5
    graph[2][6] = graph[6][2] = 1; // Edge between 2 and 6

    int target;
    printf("Enter the node to search for: ");
    scanf("%d", &target); // Input the node to search for

    bfs(graph, 0, target, num_nodes); // Start BFS from node 0

    return 0;
}

