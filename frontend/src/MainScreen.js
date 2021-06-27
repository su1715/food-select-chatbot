import React from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  SafeAreaView,
} from "react-native";

const MainScreen = ({ navigation }) => {
  function onStart() {
    navigation.navigate("Chat");
  }
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.titleWrapper}>
        <Text style={styles.title1}>뭐먹을까</Text>
        <Text style={styles.title2}>아무거나</Text>
      </View>
      <View style={styles.buttonWrapper}>
        <TouchableOpacity style={styles.startButton} onPress={onStart}>
          <Text style={styles.startButtonText}>START</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.helpButton}>
          <Text style={styles.helpButtonText}>Help</Text>
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
    fontSize: 25,
  },
  helpButtonText: {
    fontSize: 25,
  },
});
