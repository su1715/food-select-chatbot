import * as React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import * as SecureStore from "expo-secure-store";
import MainScreen from "./src/MainScreen";
import ChatScreen from "./src/ChatScreen";
import AuthScreen from "./src/AuthScreen";
import SignInScreen from "./src/SignInScreen";
import SignUpScreen from "./src/SignUpScreen";
import { url } from "./env";

const Stack = createStackNavigator();
export const AuthContext = React.createContext();

export default function App({ navigation }) {
  const [state, dispatch] = React.useReducer(
    (prevState, action) => {
      switch (action.type) {
        case "RESTORE_TOKEN":
          return {
            ...prevState,
            userToken: action.token,
            isLoading: false,
          };
        case "SIGN_IN":
          return {
            ...prevState,
            isSignout: false,
            userToken: action.token,
          };
        case "SIGN_OUT":
          return {
            ...prevState,
            isSignout: true,
            userToken: null,
          };
      }
    },
    {
      isLoading: true,
      isSignout: false,
      userToken: null,
    }
  );

  React.useEffect(() => {
    // Fetch the token from storage then navigate to our appropriate place
    const bootstrapAsync = async () => {
      let userToken;
      try {
        userToken = await SecureStore.getItemAsync("userToken");
      } catch (e) {
        // Restoring token failed
      }
      // After restoring token, we may need to validate it in production apps
      // This will switch to the App screen or Auth screen and this loading
      // screen will be unmounted and thrown away.
      dispatch({ type: "RESTORE_TOKEN", token: userToken });
    };

    bootstrapAsync();
  }, []);

  const authContext = React.useMemo(
    () => ({
      signIn: async (data) => {
        // In a production app, we need to send some data (usually username, password) to server and get a token
        // We will also need to handle errors if sign in failed
        // After getting token, we need to persist the token using `SecureStore`
        // In the example, we'll use a dummy token
        const { userId, password } = data;
        const signin_info = {
          method: "POST",
          body: JSON.stringify(data),
          headers: {
            "Content-Type": "application/json",
          },
        };
        if (userId && password) {
          console.log("signin");
          fetch(url + "/signin", signin_info)
            .then((response) => response.json())
            .then((response) => {
              if (response.result === "success") {
                SecureStore.setItemAsync("userToken", response.token);
                dispatch({ type: "SIGN_IN", token: response.token });
              } else alert(response.error);
            });
        } else {
          alert("입력 양식을 확인해주세요");
        }
      },
      signOut: async () => {
        await SecureStore.deleteItemAsync("userToken");
        dispatch({ type: "SIGN_OUT" });
      },
      signUp: async (data) => {
        // In a production app, we need to send user data to server and get a token
        // We will also need to handle errors if sign up failed
        // After getting token, we need to persist the token using `SecureStore`
        // In the example, we'll use a dummy token
        const { userId, username, password, repassword } = data;
        const signup_info = {
          method: "POST",
          body: JSON.stringify(data),
          headers: {
            "Content-Type": "application/json",
          },
        };
        let result;
        if (
          userId &&
          username &&
          password &&
          repassword &&
          password === repassword
        ) {
          console.log("signin");
          fetch(url + "/signup", signup_info)
            .then((response) => response.json())
            .then((response) => {
              if (response.result === "success") {
                SecureStore.setItemAsync("userToken", response.token);
                dispatch({ type: "SIGN_IN", token: response.token });
              } else alert(response.error);
            });
        } else {
          alert("입력 양식을 확인해주세요");
        }
      },
    }),
    []
  );
  return (
    <NavigationContainer>
      <AuthContext.Provider value={authContext}>
        <Stack.Navigator>
          {state.userToken == null ? (
            <>
              <Stack.Screen
                name="Auth"
                component={AuthScreen}
                options={{
                  headerShown: false,
                }}
              />
              <Stack.Screen
                name="SignIn"
                component={SignInScreen}
                options={{
                  headerShown: false,
                }}
              />
              <Stack.Screen
                name="SignUp"
                component={SignUpScreen}
                options={{
                  headerShown: false,
                }}
              />
            </>
          ) : (
            <>
              <Stack.Screen
                name="Main"
                component={MainScreen}
                options={{
                  headerShown: false,
                }}
                initialParams={{ token: state.userToken }}
              />
              <Stack.Screen
                name="Chat"
                component={ChatScreen}
                options={{
                  headerShown: false,
                }}
                initialParams={{ token: state.userToken }}
              />
            </>
          )}
        </Stack.Navigator>
      </AuthContext.Provider>
    </NavigationContainer>
  );
}
