import React, { ReactElement } from "react";
import { useRouter } from "next/router";

// Bootstrap
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

// Components
import Container from "../../components/styled-common/Container";
import UserProfile from "../../components/users/UserProfile";
import UserBoard from "../../components/users/UserBoard";

const Type = (): ReactElement => {
    const router = useRouter();
    const { user } = router.query;

    return (
        <Container>
            <Row className="d-flex justify-content-center w-100 mt-5 pt-5">
                <Col className="d-flex p-0 m-0" lg={9}>
                    <Row className="d-flex justify-content-center w-100">
                        <Col className="d-flex justify-content-center pl-5 pr-0" lg={3}>
                            <UserProfile username={user} />
                        </Col>
                        <Col className="d-flex justify-content-center pl-5 pr-0" lg={9}>
                            <UserBoard />
                        </Col>
                    </Row>
                </Col>
            </Row>
        </Container>
    );
};

export default Type;
