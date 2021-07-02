import React, { useState } from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  SafeAreaView,
  TextInput,
} from "react-native";

const SignInScreen = ({ navigation }) => {
  //const { signUp } = React.useContext(AuthContext);
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.title}>
        <Text style={styles.titleText}>로그인</Text>
      </View>
      <View style={styles.form}>
        <View style={styles.inputWrapper}>
          <Text style={styles.label}>아이디</Text>
          <TextInput
            placeholder="아이디"
            value={userId}
            onChangeText={setUserId}
            style={styles.textInput}
          />
        </View>
        <View style={styles.inputWrapper}>
          <Text style={styles.label}>비밀번호</Text>
          <TextInput
            placeholder="비밀번호"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            style={styles.textInput}
          />
        </View>
        <View style={styles.buttons}>
          <TouchableOpacity
            style={styles.button}
            onPress={() =>
              //signUp({ username, password })}
              {}
            }
          >
            <Text style={styles.buttonText}>로그인</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.button}
            onPress={() => navigation.navigate("Auth")}
          >
            <Text style={styles.buttonText}>취소</Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginLeft: 20,
    marginRight: 20,
  },
  title: {
    width: "100%",
    height: "15%",
    justifyContent: "center",
  },
  titleText: {
    fontSize: 30,
  },
  form: {
    width: "100%",
    alignItems: "center",
    justifyContent: "center",
  },
  inputWrapper: {
    width: "100%",
    paddingBottom: 20,
  },
  label: {
    fontSize: 20,
    paddingBottom: 6,
  },
  textInput: {
    width: "100%",
    height: 35,
    backgroundColor: "#d9d9d9",
    borderRadius: 5,
  },
  buttons: {
    width: "100%",
    height: 45,
    flexDirection: "row",
    justifyContent: "space-around",
    //backgroundColor: "pink",
  },
  button: {
    width: "30%",
    borderRadius: 10,
    borderWidth: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  buttonText: {
    fontSize: 20,
  },
});

export default SignInScreen;
