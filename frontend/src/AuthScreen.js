import React from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  SafeAreaView,
} from "react-native";

const AuthScreen = ({ navigation }) => {
  function onSignIn() {
    navigation.navigate("SignIn");
  }
  function onSignUp() {
    navigation.navigate("SignUp");
  }
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.titleWrapper}>
        <Text style={styles.title1}>뭐먹을까?</Text>
        <Text style={styles.title2}>아무거나!</Text>
      </View>
      <View style={styles.buttonWrapper}>
        <TouchableOpacity style={styles.signInButton} onPress={onSignIn}>
          <Text style={styles.signInButtonText}>로그인</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.signUpButton} onPress={onSignUp}>
          <Text style={styles.signUpButtonText}>회원가입</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

export default AuthScreen;

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
  signInButton: {
    backgroundColor: "black",
    width: "40%",
    alignItems: "center",
    borderRadius: 15,
    borderWidth: 1,
    padding: 10,
    margin: 10,
  },
  signUpButton: {
    width: "40%",
    alignItems: "center",
    borderRadius: 15,
    borderWidth: 1,
    padding: 10,
    margin: 10,
  },
  signInButtonText: {
    color: "white",
    fontSize: 25,
  },
  signUpButtonText: {
    fontSize: 25,
  },
});
