import React, { ReactElement, useEffect, useRef, useState } from "react";
import { useRouter } from "next/router";

// Bootstrap
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Form from "react-bootstrap/Form";
import axios from "axios";
import Alert from "react-bootstrap/Alert";

const RegisterCard = (): ReactElement => {
    const [isFormSubmit, setFormSubmit] = useState({ submit: false, data: { email: "", username: "", password: "" } });
    const [envobj, setEnvObj] = useState({ USER_AUTH_URL: "", USER_CRUD_URL: "" });
    const [err, setErr] = useState({ message: "", type: "" });

    const usernameInputRef = useRef<HTMLInputElement>(null);
    const emailInputRef = useRef<HTMLInputElement>(null);
    const passwordInputRef = useRef<HTMLInputElement>(null);

    const router = useRouter();
    const toggleLogin = () => router.push("/auth/login");
    const returnHome = () => router.push("/");

    useEffect(() => {
        // @ts-ignore
        const { USER_AUTH_URL, CRUD_SERVICE_URL } = process?.env?.dev;

        // TODO: dev vs prod
        if (process?.env?.NODE_ENV === "development") {
            if (process?.env) {
                setEnvObj({
                    USER_AUTH_URL: USER_AUTH_URL,
                    USER_CRUD_URL: CRUD_SERVICE_URL + "/user"
                });
            }
        } else {
            if (process?.env) {
                setEnvObj({
                    USER_AUTH_URL: USER_AUTH_URL,
                    USER_CRUD_URL: CRUD_SERVICE_URL + "/user"
                });
            }
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
                .post(envobj.USER_AUTH_URL + "register", data)
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

    const handleRegister = e => {
        e.preventDefault();

        const username = usernameInputRef?.current?.value || "";
        const email = emailInputRef?.current?.value || "";
        const password = passwordInputRef?.current?.value || "";

        setFormSubmit({ submit: true, data: { email, username, password } });
    };

    return (
        <>
            <Form onSubmit={handleRegister}>
                <Row className="d-flex flex-column">
                    {err.message && (
                        <Col>
                            <Alert variant="danger">{err.message}</Alert>
                        </Col>
                    )}
                    <Col>
                        <Form.Group>
                            <Form.Label className="m-0" column="lg" htmlFor="user-input">
                                Username
                            </Form.Label>
                            <Form.Control type="text" id="user-input" size="lg" placeholder="Username" ref={usernameInputRef} />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group>
                            <Form.Label className="m-0" column="lg" htmlFor="email-input">
                                Email
                            </Form.Label>
                            <Form.Control type="email" id="email-input" size="lg" placeholder="Email" ref={emailInputRef} />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group className="mb-5">
                            <Form.Label className="m-0" column="lg" htmlFor="password-input">
                                Password
                            </Form.Label>
                            <Form.Control id="password-input" type="password" size="lg" placeholder="Password" ref={passwordInputRef} />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Row className="btn-row-grp d-flex justify-content-between">
                            <Col className="btn-col">
                                <Button className="w-100" onClick={returnHome}>Guest</Button>
                            </Col>
                            <Col className="btn-col">
                                <Button type={"submit"} className="w-100">
                                    Register
                                </Button>
                            </Col>
                        </Row>
                    </Col>
                    <Col className="d-flex justify-content-around flex-column">
                        <p className="text-right my-4">
                            <span>Already have an account?</span>
                            <Button variant="link" className="pt-0" onClick={toggleLogin}>
                                Log In
                            </Button>
                        </p>
                        <hr className="w-100 mb-5" />
                    </Col>
                </Row>
            </Form>

            <Row className="d-flex flex-column">
                <Col className="mb-2">
                    <Button className="w-100" disabled>Sign up with Gmail</Button>
                </Col>
                <Col className="mb-2">
                    <Button className="w-100" disabled>Sign up with GitHub</Button>
                </Col>
            </Row>
        </>
    );
};

export default RegisterCard;
