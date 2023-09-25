import { FC, useState, createContext } from 'react'
import './App.css'

import { QueryForm, ImageGrid, PlayerModal, FeedbackModal } from './components'
import { FloatButton, Tooltip } from 'antd'
import { Frame } from './types'

type ImageContextType = {
    searchFrame: (path: string) => void;
    positiveFrames: string[];
    negativeFrames: string[];
    modifyFeedback: (type: number, path?: string, isNeg?: boolean, index?: number) => void;
}

export const ImageContext = createContext<ImageContextType>({
    searchFrame: () => { },
    positiveFrames: [],
    negativeFrames: [],
    modifyFeedback: () => { },
});


const App: FC = () => {
    const [paths, setPaths] = useState<string[]>(['']);
    const [isModalOpen, setModalOpen] = useState<boolean>(false);

    const [isFeedbackModalOpen, setFeedbackModalOpen] = useState<boolean>(false);

    const [frameData, setFrameData] = useState<Frame | null>(null);

    const [positiveFrames, setPositiveFrames] = useState<string[]>([]);
    const [negativeFrames, setNegativeFrames] = useState<string[]>([]);

    const modifyFeedback = (type: number, path?: string, isNeg?: boolean) => {
        // console.log(type, path, isNeg);
        if (type === 0) { // Reset
            setPositiveFrames([]);
            setNegativeFrames([]);
            return;
        }

        if (isNeg) {
            if (type > 0 && (path && !negativeFrames.includes(path))) { // If type = add and path not in negative
                setPositiveFrames(positiveFrames.filter((item) => item !== path)); // Remove from positive
                setNegativeFrames([...negativeFrames, path]); // Add to negative
            } else if (type < 0 || (path && negativeFrames.includes(path))) { // If type = remove or path in negative
                setNegativeFrames(negativeFrames.filter((item) => item !== path)); // Remove from negative
            }
        } else {
            if (type > 0 && (path && !positiveFrames.includes(path))) { // If type = add and path not in positive
                setNegativeFrames(negativeFrames.filter((item) => item !== path)); // Remove from negative
                setPositiveFrames([...positiveFrames, path]); // Add to positive
            } else if (type < 0 || (path && positiveFrames.includes(path))) { // Remove negative
                setPositiveFrames(positiveFrames.filter((item) => item !== path)); // Remove from positive
            }
        }
    }

    const searchFrame = async (path: string) => {
        try {
            const response = await fetch(
                `${process.env.API_URL}/keyframe_search?frame=${path}`,
                { method: "POST", }
            ).then(res => res.json())
            const newFrameData: Frame = {
                nearByFrames: response['near_by_keyframes'],
                index: response['index'],
                youtubeUrl: response['youtube_url'],
                playedSecond: response['played_second'],
                similarFrames: response['similar_keyframes']
            }
            setFrameData(newFrameData);
            setModalOpen(true);
        } catch (error) {
            console.log(error);
        }
    }


    const handleOpenFeedbackModal = () => {
        setFeedbackModalOpen(true)
    }

    const handleCloseFeedbackModal = () => {
        setFeedbackModalOpen(false)
    }

    const imageContextValue = {
        searchFrame,
        positiveFrames,
        negativeFrames,
        modifyFeedback,
    }

    return (
        <ImageContext.Provider value={imageContextValue}>
            <QueryForm
                setPaths={setPaths}
                positiveFrames={positiveFrames}
                negativeFrames={negativeFrames}
                resetFeedback={() => modifyFeedback(0)}
            />
            <ImageGrid paths={paths} />
            {frameData && <PlayerModal
                isOpen={isModalOpen}
                setModalOpen={setModalOpen}
                frameData={frameData}
            />}
            <FeedbackModal
                isOpen={isFeedbackModalOpen}
                onClose={handleCloseFeedbackModal}
                positiveFrames={positiveFrames}
                negativeFrames={negativeFrames}
                modifyFeedback={modifyFeedback}
            />
            <FloatButton.Group shape="circle" >
                {positiveFrames.length + negativeFrames.length > 0 && <Tooltip placement='top' title='Feedback'>
                    <FloatButton
                        badge={{ count: positiveFrames.length + negativeFrames.length, color: 'blue' }}
                        onClick={() => handleOpenFeedbackModal()}
                    />
                </Tooltip>}
                <FloatButton.BackTop />
            </FloatButton.Group>
        </ImageContext.Provider>
    )
}

export default App
