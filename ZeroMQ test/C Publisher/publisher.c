#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>

int main() {
    void *context = zmq_ctx_new();
    void *publisher = zmq_socket(context, ZMQ_PUB);
    int rc = zmq_bind(publisher, "tcp://*:5555");
    assert(rc == 0);

    while (1) {
        // Read data from your files here and store in 'data'
        // For demo, using a static string
        char data[] = "Hello, World!";

        zmq_msg_t message;
        zmq_msg_init_size(&message, strlen(data));
        memcpy(zmq_msg_data(&message), data, strlen(data));
        zmq_msg_send(&message, publisher, 0);
        zmq_msg_close(&message);

        sleep(1); // Send a message every second
        printf("Message sent successfully.\n"); // Add this line to indicate success
    }

    zmq_close(publisher);
    zmq_ctx_destroy(context);
    printf("Program finished successfully.\n"); // Add this line to indicate the program's completion
    return 0;
}
