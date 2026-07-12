import { useState } from "react";

import Workspace from "./components/Workspace";
import Header from "./components/Header";
import WelcomeScreen from "./components/WelcomeScreen";
import ChatInput from "./components/ChatInput";
import Loader from "./components/Loader";
import ClassificationCard from "./components/ClassificationCard";

import { classifyQuestion } from "./services/api";

function App() {

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  const [error, setError] = useState("");

  async function handleAsk(question) {

    setLoading(true);

    setError("");

    try {

      const response = await classifyQuestion(question);

      setResult(response);

    } catch (err) {

      setError("Unable to classify the academic doubt.");

      console.error(err);

    } finally {

      setLoading(false);

    }

  }

  return (

    <Workspace>

      <Header />

      <main
        className="
          flex-1
          flex
          justify-center
          items-start
          overflow-y-auto
          px-6
          py-8
        "
      >

        {!loading && !result && (

          <WelcomeScreen />

        )}

        {loading && (

          <Loader />

        )}

        {!loading && result && (

          <ClassificationCard result={result} />

        )}

        {error && (

          <p className="text-red-400 mt-4">
            {error}
          </p>

        )}

      </main>

      <ChatInput

        onAsk={handleAsk}

        loading={loading}

      />

    </Workspace>

  );

}

export default App;