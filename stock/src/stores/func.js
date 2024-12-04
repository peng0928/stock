function convertToChinese(numStr) {
    // 检查输入是否为有效的数字
    const num = parseFloat(numStr);
    if (isNaN(num)) {
        // 如果不是有效的数字，直接返回原字符串
        return numStr;
    }

    // 判断数字是否大于一万
    if (num > 10000) {
        // 大于一万，转换为中文表示
        return (num / 10000).toFixed(2) + '万';
    } else {
        // 不大于一万，保持原样
        return numStr;
    }
}

export default convertToChinese;