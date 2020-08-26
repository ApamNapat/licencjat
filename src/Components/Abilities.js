import DisplayTemplate from "./DisplayTemplate";
import {urlBase} from "../helpers";


class Abilities extends DisplayTemplate {
    constructor(props) {
        super(props);
        this.url = `${urlBase}abilities/${this.state.pk}/`;
        this.title = "Your Abilities";
    }

    dataProcessor = (data) => {
        return data.map((elem) => elem['ability']).sort();
    }

}


export default Abilities;