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

---

## Django Readme

> Project generated using 'django-admin startproject' with Django 5.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/

Quick-start development settings - unsuitable for production, see
https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
