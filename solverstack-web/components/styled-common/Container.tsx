import styled from "styled-components";

const StyledContainer = styled.div`
    @media (min-width: 1100px) {
        height: 100vh;
    }

    @media (max-width: 1099px) {
        height: 100%;
    }

    display: flex;
    width: 100%;
    align-items: ${props => (props.middle ? "center" : "")};

    .download-btn {
        background-color: #4CAF50;
    }
    
`;

export default StyledContainer;
