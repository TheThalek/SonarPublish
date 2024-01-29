import zmq
import time

def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    try:
        while True:
            message = subscriber.recv_string()
            print(f"Received: {message}")
            time.sleep(1)  # Optional: Control the receive rate
    except KeyboardInterrupt:
        print("Subscriber stopped.")
    finally:
        subscriber.close()
        context.term()

if __name__ == "__main__":
    main()
