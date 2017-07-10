#!/usr/bin/env bash
/Users/ikuritosensei/kafka/bin/zookeeper-server-start.sh /Users/ikuritosensei/kafka/config/zookeeper.properties
/Users/ikuritosensei/kafka/bin/kafka-server-start.sh /Users/ikuritosensei/kafka/config/server.properties
bin/kafka-topics.sh --zookeeper 163.5.220.83:2181 --delete --topic "my-topic"
bin/kafka-topics.sh \
  --zookeeper 163.5.220.83:2181 \
  --create --topic my-topic \
  --partitions 10 \
  --replication-factor 1
