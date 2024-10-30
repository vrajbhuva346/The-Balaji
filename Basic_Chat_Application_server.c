#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <winsock2.h> 
#pragma commet(lib,"ws2_32.lib")

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    
    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 3);
    
    new_socket = accept(server_fd, (struct sockaddr *)&address, (struct socklen_t*)&addrlen);
    read(new_socket, buffer, BUFFER_SIZE);
    printf("Client: %s\n", buffer);
    
    char *response = "Hello from server";
    send(new_socket, response, strlen(response), 0);
    
    close(new_socket);
    close(server_fd);
    return 0;
}
