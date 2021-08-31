import React, { useState, useCallback, useEffect } from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  SafeAreaView,
} from "react-native";
import { GiftedChat } from "react-native-gifted-chat";
import { url } from "../env";
import * as Location from "expo-location";
import Spinner from "react-native-loading-spinner-overlay";

const ChatScreen = ({ navigation, route }) => {
  const [messages, setMessages] = useState([]);
  const [latitude, setLatitude] = useState();
  const [longitude, setLongitude] = useState();
  const FIRST_MSG = "어떤 음식을 먹어볼까요?";
  const FALLBACK_MSG = "제가 제대로 이해하지 못한것 같아요.";
  const RANDOM_MSG = "랜덤으로 추천해드릴게요!";
  const BOT_USER = {
    _id: 2,
    name: "Food Bot",
    avatar: "https://i.imgur.com/7k12EPD.png",
  };
  const getLocation = async () => {
    try {
      await Location.requestForegroundPermissionsAsync();
      const location = await Location.getCurrentPositionAsync();
      setLatitude(location.coords.latitude);
      setLongitude(location.coords.longitude);
    } catch (error) {
      alert("위치 정보를 찾을 수 없습니다.");
    }
  };

  useEffect(() => {
    setMessages([
      {
        _id: 1,
        text: FIRST_MSG,
        createdAt: new Date(),
        user: BOT_USER,
      },
    ]);
    getLocation();
  }, []);

  const onSend = useCallback(
    (messages = []) => {
      setMessages((previousMessages) =>
        GiftedChat.append(previousMessages, messages)
      );
      const message_info = {
        method: "POST",
        body: JSON.stringify({
          message: messages[0],
          location: {
            latitude: latitude,
            longitude: longitude,
          },
          userId: route.params.token || "token_error",
        }),
        headers: {
          "Content-Type": "application/json",
        },
      };
      fetch(url + "/message", message_info)
        .then((response) => response.json())
        .then((response) => {
          if (response.result === "success") {
            for (let i = 0; i < response.reply.length; i++) {
              //if (i == 0)
              sendBotResponse(response.reply[i]);
            }
            if (
              response.reply[0] != FALLBACK_MSG &&
              response.reply[0] != RANDOM_MSG
            )
              sendBotQuick();
          } else alert("ChatScreen.js | line 42 fetch");
        });
    },
    [messages, latitude, longitude]
  );

  const onQuickReply = useCallback(
    (quickReply = []) => {
      let msg = {
        _id: Date.now(),
        text: quickReply[0].value,
        createdAt: new Date(),
        user: {
          _id: 1,
        },
      };
      setMessages((previousMessages) =>
        GiftedChat.append(previousMessages, [msg])
      );

      const message_info = {
        method: "POST",
        body: JSON.stringify({
          message: msg,
          location: {
            latitude: latitude,
            longitude: longitude,
          },
          userId: route.params.token || "test",
        }),
        headers: {
          "Content-Type": "application/json",
        },
      };

      fetch(url + "/message", message_info)
        .then((response) => response.json())
        .then((response) => {
          if (response.result === "success") {
            for (let i = 0; i < response.reply.length; i++) {
              sendBotResponse(response.reply[i]);
            }
            if (response.reply[0] != FIRST_MSG) sendBotQuick();
          } else alert("ChatScreen.js | fetch");
        });
    },
    [messages, latitude, longitude]
  );

  const sendBotQuick = () => {
    let msg = {
      _id: Date.now(),
      text: "어떠신가요? \n조건을 추가하려면 새로운 조건을 입력해주세요",
      createdAt: new Date(),
      quickReplies: {
        type: "radio",
        keepIt: true,
        values: [
          {
            title: "같은 조건으로 더 보여주세요",
            value: "다음",
          },
          {
            title: "다시 할래요",
            value: "재시작",
          },
        ],
      },
      user: BOT_USER,
    };
    setMessages((previousMessages) => GiftedChat.append(previousMessages, msg));
  };

  const sendBotResponse = (text) => {
    let msg = {
      _id: Date.now(),
      text,
      createdAt: new Date(),
      user: BOT_USER,
    };
    setMessages((previousMessages) => GiftedChat.append(previousMessages, msg));
  };

  function onBack() {
    navigation.navigate("Main");
  }
  function onReload() {
    navigation.navigate("Chat");
  }
  if (latitude && longitude) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <TouchableOpacity onPress={onBack}>
            <Text>뒤로</Text>
          </TouchableOpacity>
          <Text style={styles.title}>뭐먹을까? 아무거나!</Text>
          <TouchableOpacity onPress={onReload}>
            <Text>다시</Text>
          </TouchableOpacity>
        </View>
        <GiftedChat
          placeholder={"메세지를 입력하세요"}
          alwaysShowSend={true}
          messages={messages}
          textInputProps={{ keyboardAppearance: "default", autoCorrect: false }}
          onSend={(messages) => onSend(messages)}
          onQuickReply={onQuickReply}
          user={{
            _id: 1,
          }}
        />
      </SafeAreaView>
    );
  } else {
    return (
      <SafeAreaView>
        <Spinner
          visible={true}
          textContent={"위치정보를 받아오는 중입니다..."}
          textStyle={styles.spinnerTextStyle}
        />
      </SafeAreaView>
    );
  }
};

export default ChatScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    width: "100%",
    height: "6%",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingLeft: 20,
    paddingRight: 20,
    marginBottom: 5,
  },
  title: {
    fontSize: 25,
    fontWeight: "500",
  },
  spinnerTextStyle: {
    color: "#FFF",
  },
});
