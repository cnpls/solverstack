import React, { ReactElement } from "react";
import styled from "styled-components";

// Bootstrap
import Card from "react-bootstrap/Card";

// Styled
const StyledCard = styled(Card)`
    @media (max-width: 1099px) {
        width: 100%;
    }

    @media (min-width: 1100px) {
        width: 450px;
        .card-body {
            padding: 50px;
        }
    }
`;

interface Props {
    children: Array<false | ReactElement>;
}

const AuthCardContainer = (props: Props): ReactElement => {
    return (
        <StyledCard>
            <Card.Body>{props.children}</Card.Body>
        </StyledCard>
    );
};

export default AuthCardContainer;
