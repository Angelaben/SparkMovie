from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('foo', 'Coucou j''envoie ce message depuis un script Python, comme je pourrai faire pour les films')