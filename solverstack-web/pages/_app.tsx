import React, { FC } from "react";
import { AppProps } from "next/app";
import { ThemeProvider } from "styled-components";
import "bootstrap/dist/css/bootstrap.min.css";

// import { wrapper } from "../components/_store";


const theme = {
    colors: {
        primary: "black"
    }
};

const App: FC<AppProps> = ({ Component, pageProps }) => {
    return (
        <ThemeProvider theme={theme}>
            <Component {...pageProps} />
        </ThemeProvider>
    );
};

// Only uncomment this method if you have blocking data requirements for
// every single page in your application. This disables the ability to
// perform automatic static optimization, causing every page in your app to
// be server-side rendered.
//
// MyApp.getInitialProps = async (appContext) => {
//   // calls page's `getInitialProps` and fills `appProps.pageProps`
//   const appProps = await App.getInitialProps(appContext);
//
//   return { ...appProps }
// }

export default App;
