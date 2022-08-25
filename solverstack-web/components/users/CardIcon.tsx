import React from "react";
import styled from "styled-components";

// Components
import AppIcon from "../images/AppIcon";

const CustomContainer = styled.div`
    position: absolute;
    left: -25px;
    top: -25px;
`;

const CardIcon = (props) => {
    return (
        <CustomContainer>
            <AppIcon link={props.link} />
        </CustomContainer>
    );
};

export default CardIcon;
