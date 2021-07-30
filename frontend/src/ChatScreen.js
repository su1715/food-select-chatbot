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

const ChatScreen = ({ navigation }) => {
  const [messages, setMessages] = useState([]);
  const [latitude, setLatitude] = useState();
  const [longitude, setLongitude] = useState();
  const BOT_USER = {
    _id: 2,
    name: "Food Bot",
    avatar: "https://i.imgur.com/7k12EPD.png",
  };
  const getLocation = async () => {
    try {
      //TODO:위치 찾는 동안 로딩화면 띄우기
      await Location.requestForegroundPermissionsAsync();
      const location = await Location.getCurrentPositionAsync();
      setLatitude(location.coords.latitude);
      setLongitude(location.coords.longitude);
      console.log(latitude, longitude);
    } catch (error) {
      alert("위치 정보를 찾을 수 없습니다.");
    }
  };
  useEffect(() => {
    setMessages([
      {
        _id: 1,
        text: "어떤 음식을 먹어볼까요?",
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
          location: { latitude: latitude, longitude: longitude },
        }),
        headers: {
          "Content-Type": "application/json",
        },
      };
      fetch(url + "/message", message_info)
        .then((response) => response.json())
        .then((response) => {
          if (response.result === "success") sendBotResponse(response.reply);
          else alert("ChatScreen.js | line 42 fetch");
        });
    },
    [messages]
  );

  const sendBotResponse = (text) => {
    let msg = {
      _id: messages.length + 2,
      text,
      createdAt: new Date(),
      user: BOT_USER,
    };
    console.log("sendBotResponse");
    setMessages((previousMessages) => GiftedChat.append(previousMessages, msg));
  };

  function onBack() {
    navigation.navigate("Main");
  }
  function onReload() {
    navigation.navigate("Chat");
  }
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
        user={{
          _id: 1,
        }}
      />
    </SafeAreaView>
  );
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
});
