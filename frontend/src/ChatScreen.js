import React, { useState, useCallback, useEffect } from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  SafeAreaView,
} from "react-native";
import { GiftedChat } from "react-native-gifted-chat";

const ChatScreen = ({ navigation }) => {
  const [messages, setMessages] = useState([]);
  useEffect(() => {
    setMessages([
      {
        _id: 1,
        text: "어떤 음식을 먹어볼까요?",
        createdAt: new Date(),
        user: {
          _id: 2,
          name: "React Native",
          avatar: "https://placeimg.com/140/140/any",
        },
      },
    ]);
  }, []);

  const onSend = useCallback((messages = []) => {
    setMessages((previousMessages) =>
      GiftedChat.append(previousMessages, messages)
    );
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
