import React, { useContext } from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  SafeAreaView,
} from "react-native";
import { AuthContext } from "../App";
import { url } from "../env";

const MainScreen = ({ navigation, route }) => {
  const { signOut } = useContext(AuthContext);
  function onStart() {
    const message_info = {
      method: "POST",
      body: JSON.stringify({
        userId: route.params.token || "test",
      }),
      headers: {
        "Content-Type": "application/json",
      },
    };
    fetch(url + "/delete_info", message_info);
    navigation.navigate("Chat");
  }
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.titleWrapper}>
        <Text style={styles.title1}>뭐먹을까?</Text>
        <Text style={styles.title2}>아무거나!</Text>
      </View>
      <View style={styles.buttonWrapper}>
        <TouchableOpacity style={styles.startButton} onPress={onStart}>
          <Text style={styles.startButtonText}>시작</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.helpButton} onPress={signOut}>
          <Text style={styles.helpButtonText}>로그아웃</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

export default MainScreen;

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
  },
  titleWrapper: {
    width: "100%",
    height: "55%",
    alignItems: "center",
    justifyContent: "center",
  },
  buttonWrapper: {
    width: "100%",
    height: "45%",
    alignItems: "center",
    paddingTop: 90,
  },
  title1: {
    fontSize: 55,
    fontWeight: "bold",
  },
  title2: {
    fontSize: 55,
    fontWeight: "bold",
  },
  startButton: {
    backgroundColor: "black",
    width: "40%",
    alignItems: "center",
    borderRadius: 15,
    borderWidth: 1,
    padding: 10,
    margin: 10,
  },
  helpButton: {
    width: "40%",
    alignItems: "center",
    borderRadius: 15,
    borderWidth: 1,
    padding: 10,
    margin: 10,
  },
  startButtonText: {
    color: "white",
    fontSize: 27,
  },
  helpButtonText: {
    fontSize: 25,
  },
});
