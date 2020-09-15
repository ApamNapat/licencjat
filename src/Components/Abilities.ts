import DisplayTemplate from "./DisplayTemplate";
import {urlBase} from "../helpers";
import {ability} from "../interfaces";


class Abilities extends DisplayTemplate {
    constructor(props: object) {
        super(props);
        this.url = `${urlBase}abilities/${this.state.pk}/`;
        this.title = "Your Abilities";
    }

    dataProcessor = (data: ability[]): string[] => {
        return data.map((elem) => elem['ability']).sort();
    }

}


export default Abilities;