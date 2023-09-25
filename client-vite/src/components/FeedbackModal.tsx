import { FC } from 'react';
import { Modal, List, Image, Space, Button } from 'antd';
import { CloseOutlined } from '@ant-design/icons';

type FeedbackModalProps = {
    isOpen: boolean;
    onClose: () => void;
    positiveFrames: string[];
    negativeFrames: string[];
    modifyFeedback: (type: number, path?: string, isNeg?: boolean, index?: number) => void;
}

const FeedbackModal: FC<FeedbackModalProps> = ({ isOpen, onClose, positiveFrames, negativeFrames, modifyFeedback }) => {

    return (
        <Modal
            title='Relevance Feedback'
            open={isOpen}
            onCancel={onClose}
            footer={null}
        >
            <Space align='start' direction='horizontal'>
                <Space align='center' direction='vertical'>
                    <span>Negative frames</span>
                    <List
                        dataSource={negativeFrames}
                        renderItem={(item) => (
                            <List.Item  >
                                <div className='image-container'>
                                    <Image src={item} preview={false} />
                                    <Button
                                        className='top-right-button'
                                        icon={<CloseOutlined />}
                                        onClick={() => modifyFeedback(-1, item, true)}
                                    />
                                </div>
                            </List.Item>
                        )}
                    />
                </Space>
                <Space align='center' direction='vertical'>
                    <span >Positive frames</span>
                    <List
                        dataSource={positiveFrames}
                        renderItem={(item) => (
                            <List.Item className='image-container' style={{position: 'relative'}}>
                                <Image src={item} preview={false} />
                                <Button
                                    className='top-right-button'
                                    icon={<CloseOutlined />}
                                    onClick={() => modifyFeedback(-1, item, false)}
                                />
                            </List.Item>
                        )}
                    />
                </Space>
            </Space>
        </Modal>
    )
}

export default FeedbackModal;
