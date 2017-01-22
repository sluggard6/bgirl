# -*- coding:utf-8 -*-
from kafka import SimpleProducer, KafkaClient
from kafka.common import LeaderNotAvailableError
from luhu_sharper.flaskapp.orm.display_enum import DisplayEnum
from flask import current_app

class Kafka:
    
    def init_app(self, app):
        print '----------KAFKA_HOST:-------------', app.config.get('KAFKA_HOST')
        kafka = KafkaClient(app.config.get('KAFKA_HOST'))
        self.producer = SimpleProducer(kafka, async=True,
                          req_acks=SimpleProducer.ACK_AFTER_LOCAL_WRITE,
                          ack_timeout=2000,
                          sync_fail_on_error=False)

    
    class Topic(DisplayEnum):
        REGISTER = "register"
        LOGIN = "login"
        TEST_FIRST = "test_topic"
        
        __display_cn__ = {
            REGISTER: u"注册事件",
            LOGIN: u"登陆事件",
            TEST_FIRST: u'测试话题'
        }


    class Consumer_group(DisplayEnum):
        REGISTER_AWARD_GROUP = "register_award_group"
        LOGIN_AWARD_GROUP = "login_award_group"

        __display_cn__ = {
            REGISTER_AWARD_GROUP: u"注册奖励消费者",
            LOGIN_AWARD_GROUP: u"登录奖励消费者",
        }

    def send_message(self, topic, message):
        self.producer.send_messages(topic, message)

producer = Kafka()


# if __name__ == '__main__':
#     kafka.init_app(None)
#     rs = kafka.producer.send_messages("register"
#                                  , u"I'm a register".encode("utf-8"))
#     print rs
#     producer.send_message(Kafka.Topic.REGISTER, str(user))
#     print Kafka.Topic.REGISTER
#     print "success"
    
    

