/**
 * TODO: refactor for agnostic bubble maps using layers.
 * currently this file expects two hard-coded sets:
 *   - set 1: small; destinations
 *   - set 2: large; origins
 */
import MapAtlas from "./MapAtlas";
import MapCircle from "./MapCircle";
import { getAverageGeocodes } from "./MapUtils";
import { geoMercator } from "d3";


const groupClassName: string = "bubble-map";
const destCircleClassName: string = "destination";
const destCircleSize: number = 3;
const originCircleClassName: string = "origin";
const originCircleSize: number = 6;

const BubbleMap = (props) => {
    const centerMarker = getAverageGeocodes(props.destinations);
    const projection = geoMercator()
        .center([centerMarker[1], centerMarker[0]])
        .scale(props.destinations.length == 0 ? 100 : 600)
        .translate([ props.width / 2, props.height / 2 ]);
    
    if (!props.atlasJson) {
        return <pre>Loading...</pre>;
    }
    
    return (
        <svg
        height={props.height}
        width={props.width}>
            <g className={groupClassName}>
                <MapAtlas 
                atlasJson={props.atlasJson} 
                projection={projection} />
                {props.destinations.map(d => (
                    <MapCircle 
                    name={destCircleClassName} 
                    lat={d.latitude} 
                    lon={d.longitude} 
                    projection={projection}
                    size={destCircleSize} />
                ))}
                {props.origins.length > 0 &&
                    props.origins.map(d => (
                        <MapCircle 
                        name={originCircleClassName} 
                        lat={d.latitude} 
                        lon={d.longitude} 
                        projection={projection}
                        size={originCircleSize} />
                ))}
            </g>
        </svg>
    );
}

export default BubbleMap;