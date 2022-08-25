import { geoPath } from "d3";


const groupClassName: string = "atlas";
const featureColor: string = "#b8b8b8";
const featureClassName: string = "atlas-path";

const MapAtlas = (props) => {
    const atlasPath = geoPath(props.projection);
        
    return (
        <g className={groupClassName}>
            {props.atlasJson.features.map(feature => (
                <path 
                className={featureClassName}
                fill={featureColor}
                d={atlasPath(feature)} />
            ))}
        </g>
    );
}

export default MapAtlas;