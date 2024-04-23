import axios from "axios";

export async function list_all_galleries() {
    return (await axios.get("http://localhost:8081/list-all-galleries")).data
}

export async function gallery(uuid) {
    return (await axios.get(`http://localhost:8081/gallery/get/${uuid}`)).data
}

export async function gallery_add_tag(uuid, type, name) {
    return (await axios.get(`http://localhost:8081/gallery/add_tag/${uuid}/${type}/${name}`)).data
}