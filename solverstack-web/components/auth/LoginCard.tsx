import React, { ReactElement, useEffect, useRef, useState } from "react";
import { useRouter } from "next/router";
import axios from "axios";

// Bootstrap
import Alert from "react-bootstrap/Alert";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Form from "react-bootstrap/Form";
import RequestEmailModal from "./RequestEmailModal";

const LoginCard = (): ReactElement => {
    const [isFormSubmit, setFormSubmit] = useState({ submit: false, data: { username: "", email: "", password: "" } });
    const [envobj, setEnvObj] = useState({ USER_AUTH_URL: "" });
    const [err, setErr] = useState({ message: "", type: "" });
    const [modal, setModal] = useState(false);

    
    const usernameInputRef = useRef<HTMLInputElement>(null);
    const emailInputRef = useRef<HTMLInputElement>(null);
    const passwordInputRef = useRef<HTMLInputElement>(null);

    const router = useRouter();
    const toggleRegister = () => router.push("/auth/register");
    const returnHome = () => router.push("/");

    useEffect(() => {
        // @ts-ignore
        const { USER_AUTH_URL } = process?.env;
        const { query } = router;

        // TODO: dev vs prod
        if (process?.env?.NODE_ENV === "development") {
            if (process?.env) {
                setEnvObj({
                    // @ts-ignore 
                    USER_AUTH_URL: USER_AUTH_URL
                });
            }
        } else {
            if (process?.env) {
                setEnvObj({
                    // @ts-ignore 
                    USER_AUTH_URL: USER_AUTH_URL 
                });
            }
        }

        if (query.requestEmail === "true") {
            setModal(true);
        }
    }, []);

    useEffect(() => {
        /*if (envobj.USER_AUTH_URL && err.type !== "info") {
            axios
                .get(envobj.USER_AUTH_URL + "auth/local/verify")
                .then(res => {
                    // @ts-ignore
                    setErr({ message: res.message, type: "info" });
                })
                .catch(err => {
                    console.log(err);
                });
        }*/
    }, [envobj]);

    useEffect(() => {
        if (isFormSubmit.submit) {
            const data = { username: isFormSubmit.data.username, email: isFormSubmit.data.email, password: isFormSubmit.data.password };
            axios
                .post(envobj.USER_AUTH_URL + "login", data)
                .then(res => {
                    return router.push("/users/" + res.data.username);
                })
                .catch(err => {
                    setFormSubmit({ submit: false, data: { username: "", email: "", password: "" } });
                    setErr({ message: err.message, type: "danger" });
                    setTimeout(() => setErr({ message: "", type: "" }), 10000);
                });
        }
    }, [isFormSubmit.submit]);

    const handleLogin = e => {
        e.preventDefault();
        
        const username = usernameInputRef?.current?.value || "";
        const email = emailInputRef?.current?.value || "";
        const password = passwordInputRef?.current?.value || "";

        setFormSubmit({ submit: true, data: { username, email, password } });
    };

    return (
        <>
            {/*<RequestEmailModal show={modal} onHide={() => setModal(false)} envobj={envobj} />*/}
            <Form onSubmit={handleLogin}>
                <Row className="d-flex flex-column">
                    {err.message && (
                        <Col>
                            <Alert variant="danger">{err.message}</Alert>
                        </Col>
                    )}
                    <Col>
                        <Form.Group>
                            <Form.Label className="m-0" column="lg" htmlFor="username-input">
                                Username
                            </Form.Label>
                            <Form.Control
                                type="username"
                                id="username-input"
                                size="lg"
                                placeholder="Username"
                                ref={usernameInputRef}
                                disabled={err.type === "info"}
                            />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group>
                            <Form.Label className="m-0" column="lg" htmlFor="email-input">
                                Email
                            </Form.Label>
                            <Form.Control
                                type="email"
                                id="email-input"
                                size="lg"
                                placeholder="Email"
                                ref={emailInputRef}
                                disabled={err.type === "info"}
                            />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group className="mb-5">
                            <Form.Label className="m-0" column="lg" htmlFor="password-input">
                                Password
                            </Form.Label>
                            <Form.Control
                                id="password-input"
                                type="password"
                                size="lg"
                                placeholder="Password"
                                ref={passwordInputRef}
                                disabled={err.type === "info"}
                            />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Row className="btn-row-grp d-flex justify-content-between">
                            <Col className="btn-col">
                                <Button className="w-100" onClick={returnHome}>Guest</Button>
                            </Col>
                            <Col className="btn-col">
                                <Button type="submit" className="w-100">
                                    Login
                                </Button>
                            </Col>
                        </Row>
                    </Col>
                    <Col className="d-flex justify-content-around flex-column">
                        <p className="text-right my-4">
                            <span>Don&apos;t have an account?</span>
                            <Button variant="link" className="pt-0" onClick={toggleRegister}>
                                Sign Up
                            </Button>
                        </p>
                        <hr className="w-100 mb-5" />
                    </Col>
                </Row>
            </Form>

            <Row className="d-flex flex-column">
                <Col className="mb-2">
                    <Button className="w-100" disabled>Sign in with Gmail</Button>
                </Col>
                <Col className="mb-2">
                    <Button className="w-100" disabled>Sign in with GitHub</Button>
                </Col>
            </Row>
        </>
    );
};

export default LoginCard;
