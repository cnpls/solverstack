import React, { ReactElement } from "react";
import { useRouter } from "next/router";

// Bootstrap
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

// Components
import Container from "../../components/styled-common/Container";
import AuthCardContainer from "../../components/auth/AuthCardContainer";
import LoginCard from "../../components/auth/LoginCard";
import RegisterCard from "../../components/auth/RegisterCard";
import Logo from "../../components/images/Logo";

const Type = (): ReactElement => {
    const router = useRouter();
    const { type } = router.query;

    return (
        <Container middle>
            <Row className="d-flex flex-column w-100 m-0 pb-5">
                <Col className="d-flex justify-content-center align-middle pt-3 mb-4" xs="auto" sm="auto" md="auto">
                    <Row className="d-flex flex-column justify-content-center align-middle">
                        <Col className="d-flex justify-content-center">
                            <Logo />
                        </Col>
                        <Col>
                            <h3 className="mb-0">solverstack</h3>
                        </Col>
                    </Row>
                </Col>
                <Col className="d-flex justify-content-center align-middle mt-2">
                    <AuthCardContainer>
                        {type === "login" && <LoginCard />}
                        {type === "register" && <RegisterCard />}
                    </AuthCardContainer>
                </Col>
            </Row>
        </Container>
    );
};

export default Type;
