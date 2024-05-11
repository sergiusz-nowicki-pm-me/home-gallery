import { Outlet } from "react-router-dom";

export function MainPage() {
    return (
        <div className="Main-layout">
            <div className="Main-toolbar">
                <div>
                    <label htmlFor="show-thumb">Show thumbs</label>
                    <input
                        id="show-thumb"
                        type="checkbox"
                        // checked={showThumb}
                        // onClick={() => setShowThumb(!showThumb)}
                    />
                </div>
            </div>
            <div className="Main-panel">
                <Outlet />
            </div>
        </div>
    );
}
