import React, { useState, useCallback, useEffect } from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  SafeAreaView,
} from "react-native";
import { GiftedChat } from "react-native-gifted-chat";
//import { Dialogflow_V2 } from "react-native-dialogflow";
import { dialogflowConfig } from "../env";

const ChatScreen = ({ navigation }) => {
  const [messages, setMessages] = useState([]);
  const BOT_USER = {
    _id: 2,
    name: "Food Bot",
    avatar: "https://i.imgur.com/7k12EPD.png",
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
  }, []);

  // useEffect(() => {
  //   Dialogflow_V2.setConfiguration(
  //     dialogflowConfig.client_email,
  //     dialogflowConfig.private_key,
  //     Dialogflow_V2.LANG_KOREAN,
  //     dialogflowConfig.project_id
  //   );
  // }, []);

  // const handleGoogleResponse = (result) => {
  //   let text =
  //     result.queryResult.fulfillmentText || "handleGoogleResponse error";
  //   sendBotResponse(text);
  // };

  // const sendBotResponse = (text) => {
  //   let msg = {
  //     _id: messages.length + 2,
  //     text,
  //     createdAt: new Date(),
  //     user: BOT_USER,
  //   };
  //   setMessages((previousMessages) => GiftedChat.append(previousMessages, msg));
  // };

  const onSend = useCallback((messages = []) => {
    setMessages((previousMessages) =>
      GiftedChat.append(previousMessages, messages)
    );
    // console.log("send:", messages[0].text);
    // Dialogflow_V2.requestQuery(
    //   messages[0].text,
    //   (result) => handleGoogleResponse(result),
    //   (error) => console.dir(error)
    // );
  }, []);

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
