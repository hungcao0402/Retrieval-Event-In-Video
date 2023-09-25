import { FC, SetStateAction, useEffect, useState } from 'react';
import { Modal, Button, List, Divider } from 'antd';
import { LeftOutlined, RightOutlined } from '@ant-design/icons';
import ReactPlayer from 'react-player';
import { Frame } from '../types';
import { ImageWithButton } from '.'

type PlayerModalProps = {
    isOpen: boolean;
    setModalOpen: React.Dispatch<SetStateAction<boolean>>;
    frameData: Frame;
};


const PlayerModal: FC<PlayerModalProps> = ({ isOpen, setModalOpen, frameData }) => {
    const { nearByFrames, index, youtubeUrl, playedSecond, similarFrames } = frameData;
    const initIndex = index;
    const [currentIndex, setCurrentIndex] = useState<number>(initIndex);

    const handleBack = () => {
        setCurrentIndex((prev) => prev && Math.max(prev - 1, 0));
    }
    const handleForward = () => {
        setCurrentIndex((prev) => prev && Math.min(prev + 1, nearByFrames.length - 1));
    }

    const handleHideModal = () => {
        setModalOpen(false);
    }

    useEffect(() => {
        setCurrentIndex(initIndex)
    }, [initIndex])

    // switch frame back/forward when press arrow left/right
    useEffect(() => {
        const onKeyDown = (e: KeyboardEvent) => {
            switch (e.key) {
                case "ArrowLeft":
                    handleBack();
                    break;
                case "ArrowRight":
                    handleForward();
                    break;
                default:
            }
        };
        document.addEventListener("keydown", onKeyDown);
        return () => {
            document.removeEventListener("keydown", onKeyDown);
        };
    }, []);


    const colNum = 10; // Must be divisible by 2
    // console.log(currentIndex);

    return (
        frameData && <Modal
            title={`${nearByFrames[currentIndex]}`}
            open={isOpen}
            onCancel={handleHideModal}
            width={'100%'}
            footer={null}
            style={{ top: 20 }}
            destroyOnClose
        >
            <div className='flex-col'>
                <div className='flex-row' >
                    <Button icon={<LeftOutlined />} onClick={handleBack} />
                    <ImageWithButton src={nearByFrames[currentIndex]} />
                    <Button icon={<RightOutlined />} onClick={handleForward} />
                    <ReactPlayer
                        url={`${youtubeUrl}?t=${playedSecond}`}
                        playing={isOpen}
                        controls={true}
                        volume={0.25}
                        width={'100%'}
                    />
                </div>

                <div className='flex-row'>
                    {/* Previous frames */}
                    {currentIndex > 0 && <List
                        grid={{
                            gutter: 3,
                            column: Math.min(currentIndex, colNum / 2) + Math.max(colNum / 2 - Math.min(nearByFrames.length - currentIndex, colNum / 2), 0)
                        }}
                        dataSource={nearByFrames.slice(Math.max(currentIndex - (colNum - Math.min(nearByFrames.length - currentIndex, colNum / 2)), 0), currentIndex)}
                        renderItem={(path) => (
                            <List.Item>
                                <ImageWithButton src={path} />
                            </List.Item>
                        )}
                    />}
                    {/* Current  frame*/}
                    <ImageWithButton src={nearByFrames[currentIndex]} />
                    {/* Next frames */}
                    {currentIndex < nearByFrames.length - 1 && <List
                        grid={{ gutter: 3, column: Math.min(nearByFrames.length - (currentIndex + 1), colNum / 2) + Math.max(colNum / 2 - Math.min(currentIndex, colNum / 2), 0) }}
                        dataSource={nearByFrames.slice(currentIndex + 1, Math.min(nearByFrames.length, currentIndex + 1 + (colNum - Math.min(currentIndex, colNum / 2))))}
                        renderItem={(path) => (
                            <List.Item >
                                <ImageWithButton src={path} />
                            </List.Item>
                        )}
                    />}
                </div>
                <div>
                    <Divider >Similar Frames</Divider>
                    <List
                        grid={{ gutter: 8, column: 7 }}
                        dataSource={similarFrames}
                        renderItem={(path) => (
                            <List.Item >
                                <ImageWithButton src={path} />
                            </List.Item>
                        )}
                    />
                </div>
            </div>
        </Modal >
    )
}

export default PlayerModal;