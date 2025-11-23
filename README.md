## Docker + Redpanda

- To start docker container:

  ```sh
  >> docker compose up -d
  ```

- To stop docker container:

  ```sh
  >> docker compose down -v
  ```

- To check the cluster info + brokers + topics:

  ```sh
  >> docker exec -it redpanda rpk cluster info --brokers=redpanda:9092
  ```

  Output:

  ```sh
  CLUSTER
  =======
  redpanda.f19ee0b7-75d8-43f5-867f-dfa0c94a608f

  BROKERS
  =======
  ID    HOST      PORT
  0*    redpanda  9092

  TOPICS
  ======
  NAME     PARTITIONS  REPLICAS
  events   1           1
  logs     1           1
  metrics  1           1
  ```

- To produce events in redpanda:

  ```sh
  >> docker exec -it redpanda rpk topic produce events
  ```

  🔍 Breakdown

  | Part            | Meaning                                                                                  |
  | --------------- | ---------------------------------------------------------------------------------------- |
  | `docker`        | You’re using the Docker CLI.                                                             |
  | `exec`          | “Run a command inside a running container.”                                              |
  | `-it`           | -i: interactive mode, keeps STDIN open. -t: allocates a pseudo-terminal so you can type. |
  | `redpanda`      | Name of the container to run the command inside, i.e., the broker container.             |
  | `rpk`           | Redpanda’s CLI tool (like kubectl but for Redpanda).                                     |
  | `topic produce` | “Send messages into a topic.”                                                            |
  | `events`        | The name of the topic you want to publish to.                                            |

- To consume events in redpanda:

  ```sh
  >> docker exec -it redpanda rpk topic consume events
  ```

  | Part            | Meaning                             |
  | --------------- | ----------------------------------- |
  | `docker exec`   | Run something inside the container. |
  | `-it`           | Interactive terminal mode.          |
  | `redpanda`      | Again, the broker container.        |
  | `rpk`           | The CLI tool.                       |
  | `topic consume` | “Read messages from a topic.”       |
  | `events`        | Which topic to read from.           |

  Output:

  ```json
  {
    "topic": "events",
    "value": "hello",
    "timestamp": 1763918547711,
    "partition": 0,
    "offset": 6
  }
  ```

- Now, we want to produce & consume events using a python script running on local machine.

  - However, there is an issue. Initially, we have written this code within docker-compose.yml

    ```yml
    services:
        redpanda:
            ...
            command:
                ...
                - --kafka-addr=PLAINTEXT://0.0.0.0:9092
                - --advertise-kafka-addr=PLAINTEXT://redpanda:9092

        redpanda-console:
            ...
            environment:
                - KAFKA_BROKERS=redpanda:9092
    ```

  - And used this address within the script file

    ```py
    p = Producer({"bootstrap.servers": "localhost:9092"})
    ```

  - But the problem was the host was unable resolve `redpanda:9092` to `localhost:9092`, b/c localhost is not binded to redpanda.

  - So, we updated `--advertise-kafka-addr=PLAINTEXT://redpanda:9092` to `--advertise-kafka-addr=PLAINTEXT://localhost:9092`.

  - However, Inside Docker, `localhost:9092` → means inside the container, not your host. So Redpanda advertises itself as unreachable to its own clients inside the network. (Error in accessing msgs in redpanda-console's topic).

  - Hence, we needed two different addresses,

    1. For host machine (external entity) -> `localhost:9092`.
    2. For other containers (internal entity) -> `redpanda:29092`.

  - The new config becomes:

    ```yml
    services:
        redpanda:
            ...
            command:
                ...
                # LISTENERS
                - --kafka-addr=PLAINTEXT://0.0.0.0:9092,INSIDE://0.0.0.0:29092

                # ADVERTISED (what clients should use)
                - --advertise-kafka-addr=PLAINTEXT://localhost:9092,INSIDE://redpanda:29092

        redpanda-console:
            ...
            environment:
                - KAFKA_BROKERS=redpanda:29092
    ```

---

## Django Readme

> Project generated using 'django-admin startproject' with Django 5.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/

Quick-start development settings - unsuitable for production, see
https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
