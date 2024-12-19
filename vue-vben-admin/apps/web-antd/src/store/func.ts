function convertToChinese(numStr) {
  // 检查输入是否为有效的数字
  const num = parseFloat(numStr);
  if (isNaN(num)) {
    // 如果不是有效的数字，直接返回原字符串
    return numStr;
  }

  if (num > 100000000) {
    // 大于一万，转换为中文表示
    return (num / 100000000).toFixed(2) + '亿';
  }
  if (num > 10000) {
    // 大于一万，转换为中文表示
    return (num / 10000).toFixed(2) + '万';
  } else {
    // 不大于一万，保持原样
    return numStr;
  }
}

function try_toFixed(e) {
  try {
    return e.toFixed(2)
  } catch (err) {
    return e
  }
}

function splitString(str) {
  // 确保字符串长度是偶数
  str = String(str)
  if (str.length === 5) {
    str = '0' + str
  }
  // 使用slice方法每两个字符切割一次，并用join方法将它们用冒号连接
  return str.slice(0, str.length).split('').reduce((acc, cur, index) => {
    // 每两个字符添加到累加器中，并在每两个字符后添加冒号
    if (index % 2 === 0) {
      acc.push(cur + (index + 1 < str.length ? '' : ''));
    } else {
      acc[acc.length - 1] += cur;
    }
    return acc;
  }, []).join(':');
}

const StyleColor = (value = 0, large = 0, color = 'red', colorNum = 500, elseColor = 'text-green-500') => {
  if (value === 0) {
    return elseColor
  }
  return value >= large ? `text-${color}-${colorNum}` : `text-green-${colorNum}`;
};

export default {convertToChinese, try_toFixed, splitString, StyleColor};
